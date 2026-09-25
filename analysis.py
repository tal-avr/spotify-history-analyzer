def build_artist_stats(data):
    artist_time = {}
    year_artist_time = {}
    song_time = {}
    song_plays = {}
    album_time = {}
    year_time = {}
    month_time = {}

    for stream in data:
        artist = stream["master_metadata_album_artist_name"]
        ms_played = stream["ms_played"]
        year = stream["ts"][:4]
        month = stream["ts"][:7]
        song = stream["master_metadata_track_name"]
        album = stream["master_metadata_album_album_name"]

        if artist is not None:
            if artist not in artist_time:
                artist_time[artist] = 0
            artist_time[artist] += ms_played

            if year not in year_artist_time:
                year_artist_time[year] = {}

            if artist not in year_artist_time[year]:
                year_artist_time[year][artist] = 0

            year_artist_time[year][artist] += ms_played

            if song is not None:
                song_key = (song, artist)

                if song_key not in song_time:
                    song_time[song_key] = 0
                    song_plays[song_key] = 0

                song_time[song_key] += ms_played
                song_plays[song_key] += 1

            if album is not None:
                album_key = (album, artist)

                if album_key not in album_time:
                    album_time[album_key] = 0 

                album_time[album_key] += ms_played

        if year not in year_time:
            year_time[year] = 0

        year_time[year] += ms_played

        if month not in month_time:
            month_time[month] = 0

        month_time[month] += ms_played

    return artist_time, year_artist_time, song_time, song_plays, album_time, year_time, month_time


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