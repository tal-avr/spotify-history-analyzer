import matplotlib.pyplot as plt

MS_PER_HOUR = 3600000


def create_year_chart(year_time, output_dir):
    years = sorted(year_time)

    hours = []

    for year in years:
        hours.append(year_time[year] / MS_PER_HOUR)

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
        hours.append(month_time[month] / MS_PER_HOUR)

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
        listening_hours.append(ms / MS_PER_HOUR)

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
        listening_hours.append(ms / MS_PER_HOUR)

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
            artist_total_plays[artist] = artist_total_plays.get(artist, 0) + plays

    sorted_artists = sorted(
        artist_total_plays.items(),
        key=lambda item: item[1],
        reverse=True
    )

    top_artists = [
        artist
        for artist, _ in sorted_artists[:5]
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