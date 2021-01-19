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
        f"/api/v1.0/20160822<br/>"
        f"/api/v1.0/20160822/20170823<br/>"
    )

@app.route("/api/v1.0/precipitation")
def precipitation():
    # Create our session (link) from Python to the DB
    session = Session(engine)

    """Return a list of all Precipitation data"""
    # Query precipitation
    results = session.query(Measurement.date, Measurement.prcp).order_by(Measurement.date).all()

    session.close()

    # Convert list of tuples into normal list
    precip = list(np.ravel(results))

    return jsonify(precip)

@app.route("/api/v1.0/stations")
def stations():
    # Create our session (link) from Python to the DB
    session = Session(engine)

    """Return a list of all Precipitation data"""
    # Query precipitation
    results =  session.query(Station.id,Station.station, Station.name).all()

    session.close()

    # Convert list of tuples into normal list
    station_list = list(np.ravel(results))

    return jsonify(station_list)

app.route("/api/v1.0/tobs")
def tobs():
    # Create our session (link) from Python to the DB
    session = Session(engine)

    """Return a list of all Precipitation data"""
    # Query precipitation
    sel = [Station.station, Station.name, Measurement.date, Measurement.tobs]
    start_date = dt.date(2017, 8, 23) - dt.timedelta(days=366)
    results =  session.query(*sel).filter(Station.station == Measurement.station)\
        .filter(Measurement.date>start_date).filter(Station.station == 'USC00519397').order_by(Measurement.date.desc()).all()

    session.close()

    # Convert list of tuples into normal list
    last_year = list(np.ravel(results))

    return jsonify(last_year)


if __name__ == "__main__":
    app.run(debug=True)