# Spotify History Analyzer

A Python project for analyzing Spotify Streaming History and generating a personalized HTML listening report.

## Features

- Top artists, songs, and albums
- Listening trends by year and month
- Listening patterns by hour and weekday
- Song skip rate and early-skip rate
- Monthly song, artist, and album obsessions
- Artist trends over time
- Timezone-aware analysis with optional travel overrides

## How to Run

1. Place your Spotify streaming history JSON files in the `data` folder.
2. Update the file list in `main.py` if needed.
3. Optionally add travel timezone overrides.
4. Run `python3 main.py`.
5. Open the generated `report.html` file in your browser.

## Methodology

### Plays
A play is counted when a track is listened to for at least 30 seconds.

### Skips
An early skip is a manual skip before 30 seconds.

A skip is counted when a track is manually skipped either:
- before 30 seconds, or
- before two-thirds of its estimated duration.

Track duration is estimated using the median listening time of streams that ended with `trackdone`.

### Obsessions
A monthly obsession is a song, artist, or album that makes up a large share of listening activity in a given month.

### Timezones
Spotify timestamps are stored in UTC. The analyzer converts them to local time using country-based timezone mappings.

If Spotify's recorded country does not match the listener's actual location during a trip, optional travel overrides can be provided through a JSON file where the user specifies the relevant date range and timezone.

## Sample Data

The repository includes fictional sample data so the project can be tested without using personal Spotify history.

The sample files are located in the `sample` folder and include:
- generated Spotify streaming history data
- example travel timezone overrides

The sample streaming history is generated with a fixed random seed so it stays consistent across runs.

## Project Structure

- `main.py` – runs the analysis and generates the report
- `data_loader.py` – loads Spotify history and travel override files
- `analysis.py` – contains the main data-processing and analysis logic
- `report.py` – creates charts and the HTML report
- `generate_sample_data.py` – generates reproducible fictional sample data
- `sample/` – contains sample streaming history and travel override files
- `sample_output/` – contains an example HTML report and charts generated from the fictional sample data

## Status

The project is currently stable and feature-complete for its initial scope. It was built as a personal learning project.