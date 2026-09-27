from datetime import datetime
from zoneinfo import ZoneInfo
from statistics import median

MIN_EVENTS_FOR_SKIP_RATE = 40
PLAY_THRESHOLD_MS = 30_000
SKIP_DURATION_FRACTION = 2 / 3
COUNTRY_ANOMALY_MAX_GAP_SECONDS = 1800
MIN_MONTHLY_PLAYS_FOR_OBSESSION = 20
MIN_MONTHLY_ARTIST_PLAYS_FOR_OBSESSION = 50
MIN_MONTHLY_ALBUM_PLAYS_FOR_OBSESSION = 20
MS_PER_HOUR = 3600000

# This dictionary contains only selected country-to-timezone mappings.
# Add additional countries as needed.
# For countries with multiple timezones, use travel overrides instead.
COUNTRY_TIMEZONES = {
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


def prepare_travel_overrides(travel_overrides):
    for override in travel_overrides:
        override["start"] = datetime.fromisoformat(
            override["start"]
        ).date()

        override["end"] = datetime.fromisoformat(
            override["end"]
        ).date()

    return travel_overrides

def get_timezone(timestamp, country, travel_overrides):
    date = timestamp.date()

    for override in travel_overrides:
        if override["start"] <= date <= override["end"]:
            return override["timezone"]

    return COUNTRY_TIMEZONES.get(country)

def get_clean_country(data, timestamps, index):
    current_country = data[index]["conn_country"]

    if index == 0 or index == len(data) - 1:
        return current_country

    previous_country = data[index - 1]["conn_country"]
    next_country = data[index + 1]["conn_country"]

    previous_time = timestamps[index - 1]
    current_time = timestamps[index]
    next_time = timestamps[index + 1]

    time_from_previous = (current_time - previous_time).total_seconds()
    time_to_next = (next_time - current_time).total_seconds()

    if (
        previous_country == next_country
        and current_country != previous_country
        and time_from_previous <= COUNTRY_ANOMALY_MAX_GAP_SECONDS
        and time_to_next <= COUNTRY_ANOMALY_MAX_GAP_SECONDS
    ):
        return previous_country

    return current_country

def add_to_nested_dict(dictionary, outer_key, inner_key, amount):
    if outer_key not in dictionary:
        dictionary[outer_key] = {}

    if inner_key not in dictionary[outer_key]:
        dictionary[outer_key][inner_key] = 0

    dictionary[outer_key][inner_key] += amount

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

def classify_skip(stream, ms_played, duration):
    manual_skip = (
        stream["skipped"] is True
        or stream["reason_end"] == "fwdbtn"
    )

    if not manual_skip:
        return False, False

    if ms_played < PLAY_THRESHOLD_MS:
        return True, True

    if duration is not None and ms_played < SKIP_DURATION_FRACTION * duration:
        return True, False

    return False, False

def calculate_obsessions(monthly_plays, min_plays):
    obsessions = []

    for month, items in monthly_plays.items():
        total_month_plays = sum(items.values())

        for item, plays in items.items():
            if plays >= min_plays:
                percentage = plays / total_month_plays * 100
                obsessions.append(
                    (item, month, plays, percentage)
                )

    return sorted(
        obsessions,
        key=lambda item: item[3],
        reverse=True
    )

def build_listening_stats(data, travel_overrides, song_durations):
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

    timestamps = [
        datetime.fromisoformat(
            stream["ts"].replace("Z", "+00:00")
        )
        for stream in data
    ]

    for index, stream in enumerate(data):
        artist = stream["master_metadata_album_artist_name"]
        ms_played = stream["ms_played"]
        song = stream["master_metadata_track_name"]
        album = stream["master_metadata_album_album_name"]
        timestamp = timestamps[index]
        country = get_clean_country(data, timestamps, index)
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
                add_to_nested_dict(year_artist_time, year, artist, ms_played)

                year_time[year] = year_time.get(year, 0) + ms_played
                month_time[month] = month_time.get(month, 0) + ms_played
                hour_time[hour] = hour_time.get(hour, 0) + ms_played
                weekday_time[weekday] = weekday_time.get(weekday, 0) + ms_played

                if song is not None and ms_played >= PLAY_THRESHOLD_MS:
                    song_key = (song, artist)

                    add_to_nested_dict(month_song_plays, month, song_key, 1)
                    add_to_nested_dict(month_artist_plays, month, artist, 1)

                    if album is not None:
                        album_key = (album, artist)
                        add_to_nested_dict(month_album_plays, month, album_key, 1)

        # Artist total - doesn't depend on timezone
        if artist is not None:
            artist_time[artist] = artist_time.get(artist, 0) + ms_played

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

            if ms_played >= PLAY_THRESHOLD_MS:
                song_plays[song_key] += 1

            duration = song_durations.get(song_key)

            is_skip, is_early_skip = classify_skip(
                stream,
                ms_played,
                duration
            )

            if is_skip:
                song_skips[song_key] += 1

            if is_early_skip:
                song_early_skips[song_key] += 1

        # Album analysis - doesn't depend on timezone
        if album is not None and artist is not None:
            album_key = (album, artist)
            album_time[album_key] = album_time.get(album_key, 0) + ms_played

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

    song_obsessions = calculate_obsessions(
        month_song_plays,
        MIN_MONTHLY_PLAYS_FOR_OBSESSION
    )

    artist_obsessions = calculate_obsessions(
        month_artist_plays,
        MIN_MONTHLY_ARTIST_PLAYS_FOR_OBSESSION
    )

    album_obsessions = calculate_obsessions(
        month_album_plays,
        MIN_MONTHLY_ALBUM_PLAYS_FOR_OBSESSION
    )

    return {
        "artist_time": artist_time,
        "year_artist_time": year_artist_time,
        "song_time": song_time,
        "song_plays": song_plays,
        "album_time": album_time,
        "year_time": year_time,
        "month_time": month_time,
        "hour_time": hour_time,
        "weekday_time": weekday_time,
        "song_skip_rates": song_skip_rates,
        "song_early_skip_rates": song_early_skip_rates,
        "month_artist_plays": month_artist_plays,
        "song_obsessions": song_obsessions,
        "artist_obsessions": artist_obsessions,
        "album_obsessions": album_obsessions
    }

def print_top_artists(artist_times, title="TOP 10 ALL TIME:"):
    sorted_artists = sorted(
        artist_times.items(),
        key=lambda item: item[1],
        reverse=True
    )

    print(f"\n{title}")

    for artist, ms in sorted_artists[:10]:
        hours = ms / MS_PER_HOUR
        print(artist, round(hours, 2), "hours")

def print_top_artists_by_year(year_artist_time):
    for year in sorted(year_artist_time):
        print_top_artists(
            year_artist_time[year],
            f"TOP 10 IN {year}:"
        )

def print_top_songs_by_time(song_time):
    sorted_songs = sorted(
        song_time.items(),
        key=lambda item: item[1],
        reverse=True
    )

    print("\nTOP 10 SONGS BY LISTENING TIME:")

    for (song, artist), ms in sorted_songs[:10]:
        hours = ms / MS_PER_HOUR
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
        hours = ms / MS_PER_HOUR
        print(f"{album} - {artist}: {round(hours, 2)} hours")