import os
import numpy as np
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func, text
import datetime as dt
from datetime import datetime, timedelta

from flask import Flask, jsonify

#################################################
# Database Setup
#################################################
# Define the absolute path to the database file
db_path = r'C:\Users\Alyssa Jones\Desktop\sql-alchemy-challenge\sql-alchemy-challenge\Starter_Code\Resources\hawaii.sqlite'
db_path = os.path.join(os.path.dirname(__file__), 'Resources', 'hawaii.sqlite')
# create engine to hawaii.sqlite
engine = create_engine(f"sqlite:///{db_path}")
# Print the database path for debugging
print(f"Database path: {db_path}")

# Check if the database file exists
if not os.path.exists(db_path):
    print(f"Error: Database file does not exist at {db_path}")
else:
    print(f"Database file exists at {db_path}")

# Create engine to hawaii.sqlite
try:
    engine = create_engine(f"sqlite:///{db_path}")
    # Test connection by trying to execute a simple query
    with engine.connect() as connection:
        # Use the text module to execute raw SQL
        result = connection.execute(text("SELECT sqlite_version();"))
        version = result.fetchone()
        print(f"SQLite version: {version[0]}")
except sqlalchemy.exc.OperationalError as e:
    print(f"SQLAlchemy OperationalError: {e}")
    print(f"Error details can be found at: https://sqlalche.me/e/20/e3q8")
except Exception as e:
    print(f"Unexpected error: {e}")

#################################################
# Reflect an existing database into a new model
#################################################
Base = automap_base()
# Reflect the tables
Base.prepare(engine, reflect=True)

# Save references to each table
Station = Base.classes.station
Measurement = Base.classes.measurement

#################################################
# Flask Setup
#################################################
app = Flask(__name__)

#################################################
# Flask Routes
#################################################
@app.route("/")
def homepage():
    print("Server received request for homepage...")
    return (
        f"Welcome to my API! <br/>"
        f"Available Routes:<br/>"
        f"/api/v1.0/precipitation <br/>"
        f"/api/v1.0/stations <br/>"
        f"/api/v1.0/tobs <br/>"
        f"/api/v1.0/<start> <br/>"
        f"/api/v1.0/<start>/<end> <br/>"
    )

# Percipitation Analysis
@app.route("/api/v1.0/precipitation")
def precipitation():
# Creates Session (link) from Python to the Database
    session = Session(engine)
# Calculates the Date from One Year Ago from the Last Data Point in Database
    last_year = dt.date(2017, 8, 23) - dt.timedelta(days = 365)
# Querys the Past Year of Precipitation Data
    prcp_last_year = session.query(Measurement.date, Measurement.prcp).filter(Measurement.date>= last_year).all()
# Closing Session
    session.close()
# Converts Query Into Dictionary with date as Key and prcp as Value
    precipitation_data = {date: prcp for date, prcp in prcp_last_year}
# Displays Jsonify Results
    return jsonify(precipitation_data)

# Stations Dataset Analysis
from flask import jsonify, json
@app.route("/api/v1.0/stations")
def stations():
# Create Session (link) from Python to the Database
    session = Session(engine)
# Query All Stations from the Station Database
    all_stations = session.query(Station.station).distinct().all()
# Makes the Query Into a List
    all_stations = [station[0] for station in all_stations]
# Closing Session
    session.close()
# Displays Jsonify Results
    return jsonify(all_stations)

# Most-Active Station Analysis
from flask import jsonify, json
@app.route("/api/v1.0/tobs")
def active_station():
# Create Session (link) from Python to the Database
    session = Session(engine)
# Calculates the Date from One Year Ago from the Last Data Point in Database
    last_year = dt.date(2017, 8, 23) - dt.timedelta(days = 365)
# Query Dates and Temperature of the Most-Active Station from Previous Year
    most_active_year = session.query(Measurement.tobs, Measurement.date).filter(Measurement.station == 'USC00519281').\
        filter(Measurement.date>= last_year).all()
# Makes the Query Into a List
    most_active_year = [station.tobs for station in most_active_year]
# Closing Session  
    session.close()
# Displays Jsonify Results
    return jsonify(most_active_year)

# Minimum, Average, and High Temperature from Dates Greater Than or Equal to Start Date
from flask import jsonify, json
@app.route("/api/v1.0/<start_date>")
def equal_great_start(start_date):
# Create Session (link) from Python to the Database
    session = Session(engine)
# Defining Start Date
    start_date = dt.datetime.strptime(start_date,"%Y-%m-%d")
# Querying the Minimum, Average, and High Temperature from Dates Greater Than or Equal to Start Date
    temp_start_greater = session.query(func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)).\
                        filter(Measurement.date >= start_date).all()
# Closing Session
    session.close()
# Creates a Dictionary For the Temperature Data
    start_data = {"Temperature Data": []}
    for min_temp, avg_temp, max_temp in temp_start_greater:
        start_data["Temperature Data"].append({
            "Minimum Temperature": min_temp,
            "Average Temperature": avg_temp,
            "Maximum Temperature": max_temp
        })
# Displays Jsonify Data
    return jsonify(start_data)

# Minimum, Average, and High Temperature from the Start Date to the End Date
from flask import jsonify, json
@app.route("/api/v1.0/<start_date>/<end_date>")
def temp_start_end(start_date, end_date):
# Create Session (link) from Python to the Database
    session = Session(engine)
# Defining Start Date
    start_date = dt.datetime.strptime(start_date,"%Y-%m-%d")
# Defining End Date
    end_date = dt.datetime.strptime(end_date,"%Y-%m-%d")
# Querying the Minimum, Average, and High Temperature from the Start Date to the End Date
    temp_start_end = session.query(func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)).\
                        filter(Measurement.date >= start_date, Measurement.date <= end_date).all()
# Closing Session
    session.close()
# Creates a dictionary to store the temperature data
    temperature_data = []
    for min_temp, avg_temp, max_temp in temp_start_end:
        temperature_data.append({
            "Minimum Temperature": min_temp,
            "Average Temperature": avg_temp,
            "Maximum Temperature": max_temp
        })
# Displays Jsonify Data
    return jsonify({"Temperature Data": temperature_data})


# Brings up HTML Link to Run API
if __name__ == "__main__":
    app.run(debug=True)
