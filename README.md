# sqlalchemy-challenge
Climate Data Analysis and API Documentation

Project Overview
This project utilizes Python and SQLAlchemy to explore and analyze climate data stored in an SQLite database. The analysis includes precipitation and weather station data from Hawaii, providing insights through visualizations and supporting trip planning with precipitation summaries and temperature trends.

Part I: Exploratory Climate Analysis
Data Sources:

SQLite database: Resources/Hawaii.sqlite
Jupyter notebook: sqlalchemy-challenge/climate_analysis.ipnyb
Analysis Includes:

Utilization of SQLAlchemy, Pandas, and Matplotlib for data exploration and visualization.
Summary visualizations of rainfall and temperature patterns.
Support for trip planning with daily precipitation summaries and temperature trends.

Part II: Climate App
API Endpoints:

/: Home page.
/api/v1.0/precipitation: Daily precipitation totals for the last year.
/api/v1.0/stations: Active weather stations.
/api/v1.0/tobs: Daily temperature observations for the specific weather station.
/api/v1.0/trip/yyyy-mm-dd: Min, average & max temperatures for the range beginning with the provided start date through 08/23/17.
/api/v1.0/trip/yyyy-mm-dd/yyyy-mm-dd: Min, average & max temperatures for the range beginning with the provided start - end date range.
Components:

SQLite database: Resources/Hawaii.sqlite
Flask app: sqlalchemy-challenge/app.py
Usage
Setup:

Ensure Python and required dependencies are installed.
Clone or download the project repository to your local machine.
Navigate to the project directory.

While working on this module, I used Google, Xpert Learning Assistant, Chat GPT, and tutor sessions, which helped me build and run the code.
