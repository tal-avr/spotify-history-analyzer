# Spotify History Analyzer

A Python project for analyzing Spotify streaming history and generating a personalized HTML listening report, with a focus on long-term listening habits and changes in music preferences over time.

## Current Features

- Top artists, songs, and albums
- Listening trends by year and month
- Listening patterns by hour and weekday
- Song skip rate and early-skip rate
- Monthly song, artist, and album obsessions
- Artist trends over time
- Timezone-aware analysis with optional travel overrides

## Built With

- Python
- JSON
- Matplotlib
- HTML
- CSS

## How to Run

1. Place your Spotify streaming history JSON files in the `data` folder.
2. Update the file list in `main.py` if needed.
3. Optionally add travel timezone overrides.
4. Run `python3 main.py`.
5. Open the generated `report.html` file in your browser.

## How the Report Is Built

1. Spotify JSON files are loaded and combined.
2. Streaming events are cleaned, converted to local time when possible, and analyzed.
3. Charts are generated with Matplotlib.
4. Everything is combined into a standalone HTML report.

## Methodology

The current analysis focuses on music listening. Podcast streams are not included in the music-based statistics.

### Plays
A play is counted when a track is listened to for at least 30 seconds.

### Skips
An early skip is a manual skip before 30 seconds.

A skip is counted when a track is manually skipped either before 30 seconds or before two-thirds of its estimated duration.

Track duration is estimated using the median listening time of streams that ended with `trackdone`.

### Obsessions
A monthly obsession is a song, artist, or album that makes up a large share of listening activity in a given month.

### Timezones
Spotify timestamps are stored in UTC and converted to local time using country-based timezone mappings.

If Spotify's recorded country does not match the listener's actual location during a trip, travel overrides can be provided through a JSON file containing the relevant date range and timezone.

## Dataset

The project analyzes Spotify streaming-history JSON records containing listening duration, track metadata, country, platform, and playback information.

Fictional sample data and travel overrides are included in the `sample` folder for testing. A fixed random seed keeps the generated sample consistent across runs.

## Project Structure

- `main.py` – runs the analysis and generates the report
- `data_loader.py` – loads Spotify and travel data
- `analysis.py` – contains the main analysis logic
- `charts.py` – generates report charts
- `report.py` – builds the standalone HTML report
- `generate_sample_data.py` – generates reproducible fictional sample data
- `sample/` – sample input data
- `sample_output/` – example report and charts generated from the sample data

## Next Steps

Future development will focus on making the project more flexible and user-friendly, while also expanding its analytical scope. Particular emphasis will be placed on:

- improving report design and visual presentation
- allowing users to choose which analyses are included in the report
- allowing Spotify data files to be added without modifying source code
- adding further analyses of listening behavior and music preferences
- adding podcast listening analysis

## Status

The project is currently stable and feature-complete for its initial scope. It was built as a personal learning project.