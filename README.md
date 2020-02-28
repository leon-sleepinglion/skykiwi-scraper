# Skykiwi Room Scraper

## Overview

This is a side project that I built to save me the hassle of looking for room to rent in New Zealand. Skykiwi is chosen because it is one of the most active forum in New Zealand for all sorts of information including room to rent. Since the website is static in nature, everything is rendered server side, simple HTTP requests paired with HTML traversal are sufficient to scrape the data.

## Structure

To begin, we have to scrape Skykiwi for the latest data by running `scraper.py`, this will saves the data into a single file database called `entry.json`. After that, the data can be view from a simple webpage resided in `/templates` served via Flask in `app.py`.

## Requirements

- Python 3
- [Pipenv](https://pipenv.kennethreitz.org/en/latest/) (Package manager for Python, try it if you haven't)

## Run

    pipenv install
    pipenv run scraper.py
    pipenv run python app.py
