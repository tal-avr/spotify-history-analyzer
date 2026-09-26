from data_loader import load_data, load_travel_overrides
from analysis import build_artist_stats, estimate_song_durations
from report import create_html_report, create_year_chart, create_month_chart, create_hour_chart, create_weekday_chart, create_artist_trends_chart

files = [
    "data/2018_0.json",
    "data/2020_1.json",
    "data/2021_2.json",
    "data/2022_3.json",
    "data/2023_4.json",
    "data/Streaming_History_Audio_2023_5.json"
]

data = load_data(files)

travel_overrides = load_travel_overrides(
    "data/travel_overrides.json"
)

song_durations = estimate_song_durations(data)

artist_time, year_artist_time, song_time, song_plays, album_time, year_time, month_time, hour_time, weekday_time, song_skip_rates, song_early_skip_rates, month_song_plays, month_artist_plays, month_album_plays = build_artist_stats(data, travel_overrides, song_durations)

# print_top_artists(artist_time, "TOP 10 ALL TIME:")

# for year in sorted(year_artist_time):
#     print_top_artists(
#         year_artist_time[year],
#         f"TOP 10 IN {year}:"
#     )

# print_top_songs_by_time(song_time)
# print_top_songs_by_plays(song_plays)
# print_top_albums(album_time)

create_year_chart(year_time)
create_month_chart(month_time)
create_hour_chart(hour_time)
create_weekday_chart(weekday_time)
create_artist_trends_chart(month_artist_plays)
create_html_report(artist_time, year_artist_time, song_time, song_plays, album_time, year_time, month_time, song_skip_rates, song_early_skip_rates, month_song_plays, month_artist_plays, month_album_plays)
