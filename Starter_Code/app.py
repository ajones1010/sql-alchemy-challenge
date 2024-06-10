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

if __name__ == "__main__":
    app.run(debug=True)
