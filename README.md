# AnilistToMalExporter (Anime & Manga)

[![Python](https://img.shields.io/badge/Python-3.6+-blue.svg)](https://www.python.org/)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)

A Python script to export your AniList anime **and manga** lists to MyAnimeList (MAL)-compatible XML files. This is a fork of [staticaron/AnilistToMalExporter](https://github.com/staticaron/AnilistToMalExporter) with added support for exporting manga lists.

## Features
- Exports AniList anime lists to MAL XML format (e.g., `Watching`, `Completed`, `Plan to Watch`).
- **New**: Exports AniList manga lists to MAL XML format (e.g., `Reading`, `Completed`, `Plan to Read`).
- Generates separate XML files for anime (`<username>_MAL_anime.xml`) and manga (`<username>_MAL_manga.xml`).
- Maps AniList statuses, progress, scores, and start/end dates to MAL’s format.
- Simple command-line interface.

## Prerequisites
- Python 3.6 or higher
- Required libraries: `requests`, `xml.etree.ElementTree` (included in Python standard library)

## Installation
1. Clone this repository:
   ```bash
   git clone https://github.com/<your-username>/AnilistToMalExporter.git
   cd AnilistToMalExporter
