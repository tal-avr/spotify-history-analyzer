import json
import random
from datetime import datetime, timedelta

# Use a fixed seed so the sample data is reproducible across runs.
random.seed(42)

artists = {
    "Harry Potter": [
        ("Taken by a Giant Man", "Hogwarts", 210000),
        ("Quidditch", "Hogwarts", 195000),
        ("Cedric", "Hogwarts", 225000),
    ],
    "Hermione Granger": [
        ("Love, Spells", "Love, Spells", 180000),
        ("Is She Really Better Than Me", "Love, Spells", 205000),
        ("Time Goes By (and Comes Back Around)", "Love, Spells", 200000),
    ],
    "Ron Weasley": [
        ("Be Someone", "The Illuminator", 230000),
        ("Up to No Good", "The Illuminator", 215000),
        ("I Won, Haven't I", "The Illuminator", 190000),
    ],
    "Albus Dumbledore": [
        ("Power lust", "My Favorite Ballads", 240000),
        ("Second Chances", "My Favorite Ballads", 220000),
        ("The Prophecy", "My Favorite Ballads", 205000),
    ],
    "Severus Snape": [
        ("half blood prince", "doe", 275000),
        ("potions master, death eater", "doe", 211000),
        ("lily", "doe", 225000),
    ],
    "Dolores Umbridge": [
        ("I WILL HAVE ORDER", "Lies", 233000),
        ("What Cornelius Doesn't Know", "Lies", 284300),
        ("Highest Inquisitor", "Lies", 300000),
    ],
    "Minerva McGonagall": [
        ("Always Wanted to Use that Spell", "Babbity Rabbity", 143000),
        ("The Dungeons Would Do", "Babbity Rabbity", 207300),
        ("Babbling, Bumbling Band of Baboons", "Babbity Rabbity", 210000),
    ],
    "Draco Malfoy": [
        ("Good or Evil", "UNTOUCHABLE", 184390),
        ("The Malfoys", "UNTOUCHABLE", 198000),
        ("Me, Who Must Not Be Named", "UNTOUCHABLE", 179200),
    ],
    "Rubeus Hagrid": [
        ("LOVE ME JOB", "Me Songs", 144000),
        ("ARAGOG", "Me Songs", 193000),
        ("HAPPIE TIMES", "Me Songs", 249100),
    ],
    "Lord Voldemort": [
        ("The Boy Who Lived Instead of Me", "The Dark Lord (Tom's Version)", 200000),
        ("Even I Miss My Nose Sometimes", "The Dark Lord (Tom's Version)", 185000),
        ("Avada Kedavra", "The Dark Lord (Tom's Version)", 210000),
    ],
}

sample_data = []

start_date = datetime(2022, 1, 1)
number_of_streams = 6000
artist_names = list(artists.keys())

for _ in range(number_of_streams):
    timestamp = start_date + timedelta(
        days=random.randint(0, 1095),
        hours=random.randint(0, 23),
        minutes=random.randint(0, 59),
        seconds=random.randint(0, 59),
    )

    if timestamp.year == 2022:
        weights = [10, 9, 8, 6, 5, 4, 3, 2, 1, 1]
    elif timestamp.year == 2023:
        weights = [4, 7, 10, 9, 6, 5, 3, 2, 1, 1]
    else:
        weights = [2, 3, 5, 7, 10, 9, 6, 4, 2, 1]

    artist = random.choices(artist_names, weights=weights, k=1)[0]
    song, album, duration = random.choice(artists[artist])

    if timestamp.year == 2023 and timestamp.month == 7 and random.random() < 0.45:
        artist = artist_names[0]
        song, album, duration = artists[artist][0]

    is_skip = random.random() < 0.2

    if is_skip:
        ms_played = random.randint(5000, min(120000, duration - 1))
        reason_end = "fwdbtn"
        skipped = True
    else:
        ms_played = duration + random.randint(-1500, 1500)
        reason_end = "trackdone"
        skipped = False

    stream = {
        "ts": timestamp.isoformat() + "Z",
        "username": "sample_user",
        "platform": random.choice(["ios", "osx", "web_player"]),
        "ms_played": ms_played,
        "conn_country": "IL",
        "master_metadata_track_name": song,
        "master_metadata_album_artist_name": artist,
        "master_metadata_album_album_name": album,
        "spotify_track_uri": f"spotify:track:{artist}-{song}",
        "reason_start": "trackdone",
        "reason_end": reason_end,
        "shuffle": random.choice([True, False]),
        "skipped": skipped,
        "offline": False
    }

    sample_data.append(stream)

with open("sample/sample_data.json", "w", encoding="utf-8") as file:
    json.dump(sample_data, file, indent=4)