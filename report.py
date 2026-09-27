import base64

MS_PER_HOUR = 3600000


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

def create_artist_sections(artist_time, year_artist_time):
    html = ""

    sorted_artists = sorted(
        artist_time.items(),
        key=lambda item: item[1],
        reverse=True
    )

    rows = []

    for rank, (artist, ms) in enumerate(sorted_artists[:10], start=1):
        hours = ms / MS_PER_HOUR

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

        for rank, (artist, ms) in enumerate(
            sorted_year_artists[:10],
            start=1
        ):
            hours = ms / MS_PER_HOUR

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

    return html

def create_song_sections(song_time, song_plays):
    html = ""

    sorted_songs_by_time = sorted(
        song_time.items(),
        key=lambda item: item[1],
        reverse=True
    )

    rows = []

    for rank, ((song, artist), ms) in enumerate(
        sorted_songs_by_time[:10],
        start=1
    ):
        hours = ms / MS_PER_HOUR

        rows.append([
            rank,
            song,
            artist,
            round(hours, 2)
        ])

    html += "<h2>Top 10 Songs by Listening Time</h2>"

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

    for rank, ((song, artist), plays) in enumerate(
        sorted_songs_by_plays[:10],
        start=1
    ):
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

    return html

def create_album_section(album_time):

    html = ""

    sorted_albums = sorted(
            album_time.items(),
            key=lambda item: item[1],
            reverse=True
        )
    
    rows = []
    
    for rank, ((album, artist), ms) in enumerate(sorted_albums[:10], start=1):
        hours = ms / MS_PER_HOUR
    
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

    return html

def create_time_sections(year_time, month_time, output_dir):

    html = ""

    year_rows = []
    
    for year in sorted(year_time):
        hours = year_time[year] / MS_PER_HOUR
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
        hours = month_time[month] / MS_PER_HOUR
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

    return html

def create_skip_sections(song_skip_rates, song_early_skip_rates):

    html = ""

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

    return html

def create_obsessions_sections(song_obsessions, artist_obsessions, album_obsessions):

    html = ""

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
    
    rows = []
    
    for rank, (album_key, month, plays, percentage) in enumerate(album_obsessions[:10], start=1):
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

    return html

def create_artist_trends_section(output_dir):

    html = ""

    artist_trends_chart = image_to_base64(f"{output_dir}/artist_trends.png")

    html += f"""
        <h2>Top Artists Over Time</h2>
        <img class="wide-chart" src="data:image/png;base64,{artist_trends_chart}" alt="Top Artists Over Time">
    """

    return html

def create_html_report(artist_time, year_artist_time, song_time, song_plays, album_time, year_time, month_time, song_skip_rates, song_early_skip_rates, song_obsessions, artist_obsessions, album_obsessions, output_dir):
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
                margin: 20px auto;
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

    html += create_artist_sections(artist_time, year_artist_time)
    html += create_song_sections(song_time, song_plays)
    html += create_album_section(album_time)
    html += create_time_sections(year_time, month_time, output_dir)
    html += create_skip_sections(song_skip_rates, song_early_skip_rates)
    html += create_obsessions_sections(song_obsessions, artist_obsessions, album_obsessions)
    html += create_artist_trends_section(output_dir)

    html += """
    </body>
    </html>
    """

    with open(f"{output_dir}/report.html", "w", encoding="utf-8") as file:
        file.write(html)