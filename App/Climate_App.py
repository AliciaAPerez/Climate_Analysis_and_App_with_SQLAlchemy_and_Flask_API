import numpy as np

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func
import datetime as dt
from flask import Flask, jsonify

engine = create_engine("sqlite:///../Resources/hawaii.sqlite")
Base = automap_base()
Base.prepare(engine, reflect=True)
Measurement = Base.classes.measurement
Station = Base.classes.station

app = Flask(__name__)


@app.route("/")
def welcome():
    return (
        f"Welcome to the Climate Data API!<br/>"
        f"Available Routes:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        f"/api/v1.0/start/<start_date><br/>"
        f"/api/v1.0/start/<start_date>/end/<end_date><br/>"
    )

@app.route("/api/v1.0/precipitation")
def precipitation():
    # Create our session (link) from Python to the DB
    session = Session(engine)
    #start date variable
    start_date = dt.date(2017, 8, 23) - dt.timedelta(days=366)
    """Return a list of all Precipitation data for the last year"""
    # Query precipitation
    results = session.query(Measurement.date, Measurement.prcp).filter(Measurement.date > start_date).order_by(Measurement.date).all()
    #close session
    session.close()
    # Convert list
    precip = list(np.ravel(results))
    #jsonify
    return jsonify(precip)

@app.route("/api/v1.0/stations")
def stations():
    # Create our session (link) from Python to the DB
    session = Session(engine)
    """Return a list of all Station data"""
    # Query stations
    results =  session.query(Station.id,Station.station, Station.name).all()
    #close session
    session.close()
    # Convert list
    station_list = list(np.ravel(results))
    #jsonify
    return jsonify(station_list)

@app.route("/api/v1.0/tobs")
def tobs():
    #creat session
    session = Session(engine)
    #variable for date
    start_date = dt.date(2017, 8, 23) - dt.timedelta(days=366)
    #data to pull
    sel = [Station.station, Station.name, Measurement.date, Measurement.tobs]
    """Return a list of all temperature data for the past year for station USC00519281"""
    #query temperature date for last yera
    results = session.query(*sel).filter(Station.station == Measurement.station)\
        .filter(Measurement.date > start_date).filter(Station.station == 'USC00519281').order_by(Measurement.date).all()
    #close session
    session.close()
    #convert list
    last_year = list(np.ravel(results))
    #josnify
    return jsonify(last_year)


@app.route("/api/v1.0/<start>")
@app.route("/api/v1.0/<start>/<end>")
def start(start, end=None):
    #create session
    session = Session(engine)
    #variable for start date will be from user input on url
    if end:
        """Return a list of the Min, Max, and Avg Temperature for between the two dates given"""
        #query results for min,max, avg for the last year
        results = session.query(func.min(Measurement.tobs), func.max(Measurement.tobs), func.avg(Measurement.tobs)).filter(Measurement.date >= start).filter(Measurement.date <= end).all()
        #close session
        session.close()
        #convert list
        end_data = list(np.ravel(results))
        #jsonify
        return jsonify(end_data)
    else:
        """Return a list of the Min, Max, and Avg Temperature for the start date and all greater dates"""
        #query results for min, max, avg for start date
        results = session.query(func.min(Measurement.tobs), func.max(Measurement.tobs), func.avg(Measurement.tobs)).filter(Measurement.date >= start).all()
        #close session
        session.close()
        #convert list
        start_data = list(np.ravel(results))
        #jsonify
        return jsonify(start_data)

#run app
if __name__ == "__main__":
    app.run(debug=True)