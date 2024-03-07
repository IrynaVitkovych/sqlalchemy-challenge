# Import the dependencies.
import numpy as np
import pandas as import pd
import datetime as dt 

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

from flask import Flask, jsonify


#################################################
# Database Setup
#################################################
engine = create_engine("sqlite:///../Resources/hawaii.sqlite")

# reflect an existing database into a new model
Base = automap_base()
# reflect the tables
Base.prepare(autoload_with=engine)

# Save references to each table
measurement = Base.classes.measurement
station = Base.classes.station

# Create our session (link) from Python to the DB
session = Session(engine)

#################################################
# Flask Setup
#################################################
app = Flask(__name__)

#################################################
# Flask Routes
#################################################
#Home Page
@app.route("/")
def home():
    """List all available api routes."""
    return (f"Welcome in my world!<br/>"
        f"Available Routes:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        f"/api/v1.0/<start><br/>"
        f"/api/v1.0/start/<start>/end/<end>"
    )
@app.route("/api/v1.0/precipitation")
def precipitation():
    """Return the JSON representation of precipitation data for the last 12 months."""
    # Calculate the date 1 year ago from the last data point in the database
    date_year_ago = dt.date(2017, 8, 23) - dt.timedelta(days=365)

    # Query the last 12 months of precipitation data
    data_prcp = session.query(measurement.date, measurement.prcp).\
    filter(measurement.date >= date_year_ago).\
    filter(measurement.date <= dt.date(2017, 8, 23)).all()

    # Convert the query results to a dictionary
    precipitation_data = {date: prcp for date, prcp in data_prcp}

    return jsonify(precipitation_data)

@app.route("/api/v1.0/stations")
def stations():
    """Return a JSON list of stations from the dataset."""
    #Join the station and measurement tables for some of the queries.
    joined = session.query(
    station.id,
    measurement.station,
    station.name,
    station.latitude,
    station.longitude,
    station.elevation
).join(
    station,
    measurement.station == Station.station
).group_by(measurement.station).order_by(station.id).all() 
    
    # Format the results as a list of dictionaries
    stations_list = [{"name": name, "station": station, "elevation": elevation, "latitude": latitude, "longitude": longitude} for name, station, elevation, latitude, longitude in joined]

    return jsonify(stations_list)

@app.route("/api/v1.0/tobs")
def tobs():
    """Return a JSON list of temperature observations for the previous year."""
    # Using the most active station id
    # Query the last 12 months of temperature observation data for this station and plot the results as a histogram
    date_year_ago_station = dt.date(2017, 8, 18) - dt.timedelta(days=365)

    # Query the temperature observations for the most active station within the last 12 months
    results = session.query(measurement.tobs).\
    filter(measurement.station == 'USC00519281').\
    filter(measurement.date >= date_year_ago_station).\
    filter(measurement.date <= dt.date(2017, 8, 18)).all()

    # Convert the query results into a list
    temperatures = [result[0] for result in results]

    # Convert the query results to a list of dictionaries
    tobs_data = [{"date": date, "tobs": tobs} for date, tobs in results]
    return jsonify(tobs_data)

@app.route("/api/v1.0/<start>")
def calc_temps_start(start):
    """Return a JSON list of the minimum temperature, the average temperature, and the maximum temperature for a specified start date."""
    # Convert start date string to datetime object
    start_date = dt.datetime.strptime(start, "%Y-%m-%d").date()

    # Query TMIN, TAVG, and TMAX for dates greater than or equal to the start date
    results = session.query(func.min(measurement.tobs), func.avg(measurement.tobs), func.max(measurement.tobs)).\
        filter(measurement.date >= start_date).all()

    # Convert the query results to a list of dictionaries
    temp_data = []
    for Tmin, Tavg, Tmax in results:
        temp_dict = {}
        temp_dict["TMIN"] = Tmin
        temp_dict["TAVG"] = Tavg
        temp_dict["TMAX"] = Tmax
        temp_data.append(temp_dict)

    return jsonify(temp_data)

@app.route("/api/v1.0/<start>/<end>")
def calc_temps_start_end(start, end):
    """Return a JSON list of the minimum temperature, the average temperature, and the maximum temperature for a specified start-end range."""
    # Convert start and end date strings to datetime objects
    start_date = dt.datetime.strptime(start, "%Y-%m-%d").date()
    end_date = dt.datetime.strptime(end, "%Y-%m-%d").date()

    # Query TMIN, TAVG, and TMAX for dates within the start-end range
    results = session.query(func.min(measurement.tobs), func.avg(measurement.tobs), func.max(measurement.tobs)).\
        filter(measurement.date >= start_date).\
        filter(measurement.date <= end_date).all()

    # Convert the query results to a list of dictionaries
    temp_data = []
    for Tmin, Tavg, Tmax in results:
        temp_dict = {}
        temp_dict["TMIN"] = Tmin
        temp_dict["TAVG"] = Tavg
        temp_dict["TMAX"] = Tmax
        temp_data.append(temp_dict)

    return jsonify(temp_data)

if __name__ == "__main__":
    app.run(debug=True)