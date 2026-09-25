import matplotlib.pyplot as plt

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

def create_html_report(artist_time, year_artist_time, song_time, song_plays, album_time, year_time, month_time):
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

    html += """
        <img src="year_listening.png" alt="Listening Time by Year">
        """
    
    html += "<h2>Listening Time by Month</h2>"
    
    html += create_table(
        ["Month", "Hours"],
        month_rows
    )

    html += """
        <img src="month_listening.png" alt="Listening Time by Month">
        """

    html += """
    </body>
    </html>
    """

    with open("report.html", "w", encoding="utf-8") as file:
        file.write(html)


def create_year_chart(year_time):
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

    plt.savefig("year_listening.png")
    plt.close()

def create_month_chart(month_time):
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

    plt.savefig("month_listening.png")
    plt.close()