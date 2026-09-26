from datetime import datetime
from sqlite3.dbapi2 import Timestamp
from zoneinfo import ZoneInfo
from statistics import median

MIN_EVENTS_FOR_SKIP_RATE = 40

# This dictionary contains only selected country-to-timezone mappings.
# Add additional countries as needed.
# For countries with multiple timezones, use travel overrides instead.
country_timezones = {
    "IL": "Asia/Jerusalem",
    "GB": "Europe/London",
    "FR": "Europe/Paris",
    "CZ": "Europe/Prague",
    "RO": "Europe/Bucharest",
    "CH": "Europe/Zurich",
    "AT": "Europe/Vienna",
    "NL": "Europe/Amsterdam",
    "DE": "Europe/Berlin"
}

def get_timezone(timestamp, country, travel_overrides):
    date = timestamp.date()

    for override in travel_overrides:
        start_date = datetime.fromisoformat(
            override["start"]
        ).date()

        end_date = datetime.fromisoformat(
            override["end"]
        ).date()

        if start_date <= date <= end_date:
            return override["timezone"]

    return country_timezones.get(country)

def get_clean_country(data, index):
    current_country = data[index]["conn_country"]

    if index == 0 or index == len(data) - 1:
        return current_country

    previous_country = data[index - 1]["conn_country"]
    next_country = data[index + 1]["conn_country"]

    previous_time = datetime.fromisoformat(
        data[index - 1]["ts"].replace("Z", "+00:00")
    )

    current_time = datetime.fromisoformat(
        data[index]["ts"].replace("Z", "+00:00")
    )

    next_time = datetime.fromisoformat(
        data[index + 1]["ts"].replace("Z", "+00:00")
    )

    time_from_previous = (current_time - previous_time).total_seconds()
    time_to_next = (next_time - current_time).total_seconds()

    if (
        previous_country == next_country
        and current_country != previous_country
        and time_from_previous <= 1800
        and time_to_next <= 1800
    ):
        return previous_country

    return current_country

def estimate_song_durations(data):
    duration_samples = {}

    for stream in data:
        song = stream["master_metadata_track_name"]
        artist = stream["master_metadata_album_artist_name"]
        ms_played = stream["ms_played"]

        if (
            song is not None
            and artist is not None
            and stream["reason_end"] == "trackdone"
        ):
            song_key = (song, artist)

            if song_key not in duration_samples:
                duration_samples[song_key] = []

            duration_samples[song_key].append(ms_played)

    song_durations = {}

    for song_key, samples in duration_samples.items():
        song_durations[song_key] = median(samples)

    return song_durations

def build_artist_stats(data, travel_overrides, song_durations):
    artist_time = {}
    year_artist_time = {}
    song_time = {}
    song_plays = {}
    album_time = {}
    year_time = {}
    month_time = {}
    hour_time = {}
    weekday_time = {}
    month_song_plays = {}
    month_artist_plays = {}
    month_album_plays = {}

    song_events = {}
    song_skips = {}
    song_early_skips = {}

    for index, stream in enumerate(data):
        artist = stream["master_metadata_album_artist_name"]
        ms_played = stream["ms_played"]
        song = stream["master_metadata_track_name"]
        album = stream["master_metadata_album_album_name"]
        timestamp = datetime.fromisoformat(
            stream["ts"].replace("Z", "+00:00")
        )

        country = get_clean_country(data, index)
        timezone_name = get_timezone(
            timestamp,
            country,
            travel_overrides
        )

        # Time-based analysis - depends on timezone
        if timezone_name is not None:
            local_time = timestamp.astimezone(
                ZoneInfo(timezone_name)
            )

            year = str(local_time.year)
            month = local_time.strftime("%Y-%m")
            hour = local_time.hour
            weekday = local_time.strftime("%A")

            if artist is not None:
                if year not in year_artist_time:
                    year_artist_time[year] = {}

                if artist not in year_artist_time[year]:
                    year_artist_time[year][artist] = 0

                year_artist_time[year][artist] += ms_played

                if year not in year_time:
                    year_time[year] = 0

                year_time[year] += ms_played

                if month not in month_time:
                    month_time[month] = 0

                month_time[month] += ms_played

                if hour not in hour_time:
                    hour_time[hour] = 0

                hour_time[hour] += ms_played

                if weekday not in weekday_time:
                    weekday_time[weekday] = 0

                weekday_time[weekday] += ms_played

                if song is not None and ms_played >= 30000:
                    song_key = (song, artist)

                    if month not in month_song_plays:
                        month_song_plays[month] = {}

                    if song_key not in month_song_plays[month]:
                        month_song_plays[month][song_key] = 0

                    month_song_plays[month][song_key] += 1

                    if month not in month_artist_plays:
                        month_artist_plays[month] = {}

                    if artist not in month_artist_plays[month]:
                        month_artist_plays[month][artist] = 0

                    month_artist_plays[month][artist] += 1

                    if artist is not None:
                        album_key = (album, artist)

                        if month not in month_album_plays:
                            month_album_plays[month] = {}

                        if album_key not in month_album_plays[month]:
                            month_album_plays[month][album_key] = 0

                        month_album_plays[month][album_key] += 1

        # Artist total - doesn't depend on timezone
        if artist is not None:
            if artist not in artist_time:
                artist_time[artist] = 0
            
            artist_time[artist] += ms_played

        # Song analysis - doesn't depend on timezone
        if song is not None and artist is not None:
            song_key = (song, artist)
        
            if song_key not in song_events:
                song_events[song_key] = 0
                song_time[song_key] = 0
                song_plays[song_key] = 0
                song_skips[song_key] = 0
                song_early_skips[song_key] = 0

            song_events[song_key] += 1
            song_time[song_key] += ms_played

            if ms_played >= 30000:
                song_plays[song_key] += 1

            manual_skip = (
                stream["skipped"] is True
                or stream["reason_end"] == "fwdbtn"
            )

            if manual_skip:
                duration = song_durations.get(song_key)

                if ms_played < 30000:
                    song_early_skips[song_key] += 1
                    song_skips[song_key] += 1

                elif duration is not None and ms_played < (2 / 3) * duration:
                    song_skips[song_key] += 1

        # Album analysis - doesn't depend on timezone
        if album is not None and artist is not None:
            album_key = (album, artist)
        
            if album_key not in album_time:
                album_time[album_key] = 0 
        
            album_time[album_key] += ms_played

    song_skip_rates = {}
    song_early_skip_rates = {}

    for song_key in song_events:
        events = song_events[song_key]

        if events >= MIN_EVENTS_FOR_SKIP_RATE:
            song_skip_rates[song_key] = (
                song_skips[song_key] / events
            )

            song_early_skip_rates[song_key] = (
                song_early_skips[song_key] / events
            )

    return artist_time, year_artist_time, song_time, song_plays, album_time, year_time, month_time, hour_time, weekday_time, song_skip_rates, song_early_skip_rates, month_song_plays, month_artist_plays, month_album_plays

def print_top_artists(artist_times, title):
    sorted_artists = sorted(
        artist_times.items(),
        key=lambda item: item[1],
        reverse=True
    )

    print(f"\n{title}")

    for artist, ms in sorted_artists[:10]:
        hours = ms / 3600000
        print(artist, round(hours, 2), "hours")

def print_top_songs_by_time(song_time):
    sorted_songs = sorted(
        song_time.items(),
        key=lambda item: item[1],
        reverse=True
    )

    print("\nTOP 10 SONGS BY LISTENING TIME:")

    for (song, artist), ms in sorted_songs[:10]:
        hours = ms / 3600000
        print(f"{artist} - {song}: {round(hours, 2)} hours")

def print_top_songs_by_plays(song_plays):
    sorted_songs = sorted(
        song_plays.items(),
        key=lambda item: item[1],
        reverse=True
    )

    print("\nTOP 10 SONGS BY NUMBER OF PLAYS:")

    for (song, artist), plays in sorted_songs[:10]:
        print(f"{artist} - {song}: {plays} plays")

def print_top_albums(album_time):
    sorted_albums = sorted(
        album_time.items(),
        key=lambda item: item[1],
        reverse=True
    )

    print("\nTOP 10 ALBUMS BY LISTENING TIME:")

    for (album, artist), ms in sorted_albums[:10]:
        hours = ms / 3600000
        print(f"{album} - {artist}: {round(hours, 2)} hours")