import os

from data_loader import load_data, load_travel_overrides
from analysis import build_listening_stats, estimate_song_durations, prepare_travel_overrides
from report import create_html_report
from charts import create_year_chart, create_month_chart, create_hour_chart, create_weekday_chart, create_artist_trends_chart


def main():

    files = [
        "sample/sample_data.json"
    ]

    output_dir = "sample_output"
    os.makedirs(output_dir, exist_ok=True)

    data = load_data(files)

    travel_overrides = load_travel_overrides(
        "sample/sample_travel_overrides.json"
    )

    travel_overrides = prepare_travel_overrides(
        travel_overrides
    )

    song_durations = estimate_song_durations(data)

    stats = build_listening_stats(data, travel_overrides, song_durations)

    create_year_chart(stats["year_time"], output_dir)
    create_month_chart(stats["month_time"], output_dir)
    create_hour_chart(stats["hour_time"], output_dir)
    create_weekday_chart(stats["weekday_time"], output_dir)
    create_artist_trends_chart(stats["month_artist_plays"], output_dir)
    create_html_report(
        stats["artist_time"], stats["year_artist_time"], stats["song_time"],
        stats["song_plays"], stats["album_time"], stats["year_time"], stats["month_time"],
        stats["song_skip_rates"], stats["song_early_skip_rates"],
        stats["song_obsessions"], stats["artist_obsessions"], stats["album_obsessions"],
        output_dir
    )


if __name__ == "__main__":
    main()