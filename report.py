import matplotlib.pyplot as plt
import base64

MIN_MONTHLY_PLAYS_FOR_OBSESSION = 20
MIN_MONTHLY_ARTIST_PLAYS_FOR_OBSESSION = 50
MIN_MONTHLY_ALBUM_PLAYS_FOR_OBSESSION = 20

def image_to_base64(filename):
    with open(filename, "rb") as image_file:
        encoded = base64.b64encode(image_file.read()).decode("utf-8")
    return encoded

def create_table(headers, rows, table_class=""):
    html = f'<table class="{table_class}">'

    html += "<tr>"
    for header in headers:
        html += f"<th>{header}</th>"
    html += "</tr>"

    for row in rows:
        html += "<tr>"

        for value in row:
            html += f"<td>{value}</td>"

        html += "</tr>"

    html += "</table>"

    return html

def create_html_report(artist_time, year_artist_time, song_time, song_plays, album_time, year_time, month_time, song_skip_rates, song_early_skip_rates, month_song_plays, month_artist_plays, month_album_plays, output_dir):
    html = """
    <html>
    <head>
        <style>
            body {
                font-family: Arial;
                max-width: 900px;
                margin: auto;
                padding-top: 30px;
            }

            h1 {
                text-align: center;
            }

            table {
                width: 100%;
                border-collapse: collapse;
            }

            th, td {
                padding: 10px;
                border-bottom: 1px solid #ddd;
                text-align: left;
            }

            .year-table {
                font-size: 14px;
            }

            .year-title {
                font-size: 20px;
            }

            img {
                width: 100%;
                max-width: 800px;
                display: block;
                margin: 20px auto
            }

            .wide-chart {
                width: 1100px;
                max-width: 82vw;
                position: relative;
                left: 50%;
                transform: translateX(-50%);
            }

        </style>
    </head>

    <body>
        <h1>Spotify Listening Report</h1>
    """
    sorted_artists = sorted(
            artist_time.items(),
            key=lambda item: item[1],
            reverse=True
        )

    rows = []

    for rank, (artist, ms) in enumerate(sorted_artists[:10], start=1):
        hours = ms / 3600000

        rows.append([
            rank,
            artist,
            round(hours, 2)
        ])

    html += "<h2>Top 10 Artists All Time</h2>"

    html += create_table(
        ["Rank", "Artist", "Hours"],
        rows
    )

    for year in sorted(year_artist_time):
        sorted_year_artists = sorted(
            year_artist_time[year].items(),
            key=lambda item: item[1],
            reverse=True
        )

        rows = []

        for rank, (artist, ms) in enumerate(sorted_year_artists[:10], start=1):
            hours = ms / 3600000

            rows.append([
                rank,
                artist,
                round(hours, 2)
            ])

        html += f'<h2 class="year-title">Top 10 in {year}</h2>'

        html += create_table(
            ["Rank", "Artist", "Hours"],
            rows,
            "year-table"
        )

    sorted_songs_by_time = sorted(
        song_time.items(),
        key=lambda item: item[1],
        reverse=True
    )

    rows = []

    for rank, ((song, artist), ms) in enumerate(sorted_songs_by_time[:10], start=1):
            hours = ms / 3600000
    
            rows.append([
                rank,
                song,
                artist,
                round(hours, 2)
            ])

    html += "<h2>Top 10 Songs by Listening Time<h2>"

    html += create_table(
        ["Rank", "Song", "Artist", "Hours"],
        rows
    )

    sorted_songs_by_plays = sorted(
        song_plays.items(),
        key=lambda item: item[1],
        reverse=True
    )

    rows = []

    for rank, ((song, artist), plays) in enumerate(sorted_songs_by_plays[:10], start=1):

            rows.append([
                rank,
                song,
                artist,
                plays
            ])
                
    html += "<h2>Top 10 Songs by Number of Plays</h2>"

    html += create_table(
        ["Rank", "Song", "Artist", "Plays"],
        rows
    )

    sorted_albums = sorted(
        album_time.items(),
        key=lambda item: item[1],
        reverse=True
    )

    rows = []

    for rank, ((album, artist), ms) in enumerate(sorted_albums[:10], start=1):
        hours = ms / 3600000

        rows.append([
            rank,
            album,
            artist,
            round(hours, 2)
        ])

    html += "<h2>Top 10 Albums by Listening Time</h2>"

    html += create_table(
        ["Rank", "Album", "Artist", "Hours"],
        rows
    )

    year_rows = []

    for year in sorted(year_time):
         hours = year_time[year] / 3600000
         year_rows.append([
              year,
              round(hours, 2)
         ])

    html += "<h2>Listening Time by Year</h2>"

    html += create_table(
         ["Year", "Hours"],
         year_rows
    )

    month_rows = []
    
    for month in sorted(month_time):
        hours = month_time[month] / 3600000
        month_rows.append([
            month,
            round(hours, 2)
        ])

    year_chart = image_to_base64(f"{output_dir}/year_listening.png")

    html += f"""
        <img src="data:image/png;base64,{year_chart}" alt="Listening Time by Year">
        """
    
    html += "<h2>Listening Time by Month</h2>"
    
    html += create_table(
        ["Month", "Hours"],
        month_rows
    )

    month_chart = image_to_base64(f"{output_dir}/month_listening.png")

    html += f"""
        <img src="data:image/png;base64,{month_chart}" alt="Listening Time by Month">
    """

    hour_chart = image_to_base64(f"{output_dir}/hour_listening.png")

    html += f"""
        <h2>Listening Time by Hour of the Day</h2>
        <img src="data:image/png;base64,{hour_chart}" alt="Listening Time by Hour">
    """

    weekday_chart = image_to_base64(f"{output_dir}/weekday_listening.png")

    html += f"""
        <h2>Listening Time by Day of the Week</h2>
        <img src="data:image/png;base64,{weekday_chart}" alt="Listening Time by Weekday">
    """

    sorted_skip_rates = sorted(
        song_skip_rates.items(),
        key=lambda item: item[1],
        reverse=True
    )

    rows = []

    for rank, ((song, artist), rate) in enumerate(sorted_skip_rates[:10], start=1):
        rows.append([
            rank,
            song,
            artist,
            round(rate * 100)
        ])

    html += "<h2>Top 10 Songs by Skip Rate</h2>"

    html += create_table(
        ["Rank", "Song", "Artist", "Skip Rate (%)"],
        rows
    )

    sorted_early_skip_rates = sorted(
        song_early_skip_rates.items(),
        key=lambda item: item[1],
        reverse=True
    )

    rows = []

    for rank, ((song, artist), rate) in enumerate(
        sorted_early_skip_rates[:10],
        start=1
    ):
        rows.append([
            rank,
            song,
            artist,
            round(rate * 100)
        ])

    html += "<h2>Top 10 Songs by Early Skip Rate</h2>"

    html += create_table(
        ["Rank", "Song", "Artist", "Early Skip Rate (%)"],
        rows
    )

    song_obsessions = []

    for month, songs in month_song_plays.items():
        total_month_plays = sum(songs.values())

        for song_key, plays in songs.items():
            if plays >= MIN_MONTHLY_PLAYS_FOR_OBSESSION:
                percentage = plays / total_month_plays * 100

                song_obsessions.append(
                    (song_key, month, plays, percentage)
                )

    song_obsessions = sorted(
        song_obsessions,
        key=lambda item: item[3],
        reverse=True
    )

    rows = []

    for rank, (song_key, month, plays, percentage) in enumerate(
        song_obsessions[:10],
        start=1
    ):
        song, artist = song_key

        rows.append([
            rank,
            song,
            artist,
            month,
            plays,
            round(percentage)
        ])

    html += "<h2>Top Song Obsessions by Month</h2>"

    html += create_table(
        ["Rank", "Song", "Artist", "Month", "Plays", "Share of Month (%)"],
        rows
    )

    artist_obsessions = []

    for month, artists in month_artist_plays.items():
        total_month_plays = sum(artists.values())

        for artist, plays in artists.items():
            if plays >= MIN_MONTHLY_ARTIST_PLAYS_FOR_OBSESSION:
                percentage = plays / total_month_plays * 100

                artist_obsessions.append(
                    (artist, month, plays, percentage)
                )

    artist_obsessions = sorted(
        artist_obsessions,
        key=lambda item: item[3],
        reverse=True
    )

    rows = []
    
    for rank, (artist, month, plays, percentage) in enumerate(
        artist_obsessions[:10],
        start=1
    ):
    
        rows.append([
            rank,
            artist,
            month,
            plays,
            round(percentage)
        ])
    
    html += "<h2>Top Artist Obsessions by Month</h2>"
    
    html += create_table(
        ["Rank", "Artist", "Month", "Plays", "Share of Month (%)"],
        rows
    )

    album_obsessions = []

    for month, albums in month_album_plays.items():
        total_month_plays = sum(albums.values())

        for album_key, plays in albums.items():
            if plays >= MIN_MONTHLY_ALBUM_PLAYS_FOR_OBSESSION:
                percentage = plays / total_month_plays * 100

                album_obsessions.append(
                    (album_key, month, plays, percentage)
                )

    album_obsessions = sorted(
        album_obsessions,
        key=lambda item: item[3],
        reverse=True
    )

    rows = []

    for rank, (album_key, month, plays, percentage) in enumerate(
        album_obsessions[:10],
        start=1
    ):
        album, artist = album_key

        rows.append([
            rank,
            album,
            artist,
            month,
            plays,
            round(percentage)
        ])

    html += "<h2>Top Album Obsessions by Month</h2>"

    html += create_table(
        ["Rank", "Album", "Artist", "Month", "Plays", "Share of Month (%)"],
        rows
    )

    artist_trends_chart = image_to_base64(f"{output_dir}/artist_trends.png")

    html += f"""
        <h2>Top Artists Over Time</h2>
        <img class="wide-chart" src="data:image/png;base64,{artist_trends_chart}" alt="Top Artists Over Time">
    """

    html += """
    </body>
    </html>
    """

    with open(f"{output_dir}/report.html", "w", encoding="utf-8") as file:
        file.write(html)


def create_year_chart(year_time, output_dir):
    years = sorted(year_time)

    hours = []

    for year in years:
        hours.append(year_time[year] / 3600000)

    plt.figure()

    plt.bar(years, hours)

    plt.title("Listening Time by Year")
    plt.xlabel("Year")
    plt.ylabel("Hours")

    plt.tight_layout()

    plt.savefig(f"{output_dir}/year_listening.png")
    plt.close()

def create_month_chart(month_time, output_dir):
    months = sorted(month_time)

    hours = []

    for month in months:
        hours.append(month_time[month] / 3600000)

    plt.figure(figsize=(12, 5))

    plt.plot(months, hours)

    plt.title("Listening Time by Month")
    plt.xlabel("Month")
    plt.ylabel("Hours")

    tick_positions = range(0, len(months), 6)

    plt.xticks(
         tick_positions,
         [months[i] for i in tick_positions],
         rotation=45
    )

    plt.tight_layout()

    plt.savefig(f"{output_dir}/month_listening.png")
    plt.close()

def create_hour_chart(hour_time, output_dir):
    hours = list(range(24))

    listening_hours = []

    for hour in hours:
        ms = hour_time.get(hour, 0)
        listening_hours.append(ms / 3600000)

    plt.figure(figsize=(12, 5))

    plt.bar(hours, listening_hours)

    plt.title("Listening Time by Hour of Day")
    plt.xlabel("Hour")
    plt.ylabel("Hours")

    plt.xticks(hours)

    plt.tight_layout()

    plt.savefig(f"{output_dir}/hour_listening.png")
    plt.close()

def create_weekday_chart(weekday_time, output_dir):
    weekdays = [
        "Sunday",
        "Monday",
        "Tuesday",
        "Wednesday",
        "Thursday",
        "Friday",
        "Saturday"
    ]

    listening_hours = []

    for day in weekdays:
        ms = weekday_time.get(day, 0)
        listening_hours.append(ms / 3600000)

    plt.figure(figsize=(10, 5))

    plt.bar(weekdays, listening_hours)

    plt.title("Listening Time by Day of Week")
    plt.xlabel("Day")
    plt.ylabel("Hours")

    plt.xticks(rotation=45)

    plt.tight_layout()

    plt.savefig(f"{output_dir}/weekday_listening.png")
    plt.close()

def create_artist_trends_chart(month_artist_plays, output_dir):
    artist_total_plays = {}

    for artists in month_artist_plays.values():
        for artist, plays in artists.items():
            if artist not in artist_total_plays:
                artist_total_plays[artist] = 0

            artist_total_plays[artist] += plays

    sorted_artists = sorted(
        artist_total_plays.items(),
        key=lambda item: item[1],
        reverse=True
    )

    top_artists = [
        artist
        for artist, plays in sorted_artists[:5]
    ]

    months = sorted(month_artist_plays)

    plt.figure(figsize=(16, 7))

    for artist in top_artists:
        monthly_plays = []

        for month in months:
            plays = month_artist_plays[month].get(artist, 0)
            monthly_plays.append(plays)

        plt.plot(
            months,
            monthly_plays,
            label=artist,
            linewidth=2
        )

    tick_positions = range(0, len(months), 12)

    plt.xticks(
        tick_positions,
        [months[i] for i in tick_positions],
        rotation=45
    )

    plt.title("Top Artists Over Time")
    plt.xlabel("Month")
    plt.ylabel("Plays")

    plt.grid(axis="y", alpha=0.3)
    plt.legend()
    plt.tight_layout()

    plt.savefig(f"{output_dir}/artist_trends.png")
    plt.close()
