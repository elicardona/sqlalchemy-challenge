import numpy as np
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func
import datetime as dt
import pandas as pd
from flask import Flask
from flask.json import jsonify

engine = create_engine("sqlite:///Resources/hawaii.sqlite")
conn= engine.connect()

#data= pd.read_sql("SELECT * FROM measurement",conn)
app = Flask(__name__)

Base=automap_base()
Base.prepare(engine,reflect=True)
Base.classes.keys()

measurement=Base.classes.measurement
station=Base.classes.station


@app.route("/")
def home():
    return (f"Available Routes:<br/>"
            f"/api/v1.0/precipitation<br/>"
            f"/api/v1.0/stations<br/>"
            f"/api/v1.0/tobs<br/>"
            f"/api/v1.0/start<br/>"
            f"/api/v1.0/start/end"

    )


@app.route("/api/v1.0/precipitation")
def precipitation():

    session=Session(engine)
    precipitation=session.query(measurement.date,measurement.prcp).all()
    session.close()

    prcp_values=[]
    for date,prcp in precipitation:
        measurement_dict={date:prcp}
        prcp_values.append(measurement_dict)

    return jsonify(prcp_values)


@app.route("/api/v1.0/stations")
def stations():
    session= Session(engine)
    stations= session.query(station.station).all()
    session.close()
    station_names=list(np.ravel(stations))
    return jsonify(station_names)


@app.route("/api/v1.0/tobs")
def tobs():
    session= Session(engine)
    temp_results= session.query(measurement.date,measurement.tobs).filter(measurement.date>'2016-8-23').filter(measurement.station=='USC00519281').order_by(measurement.date).all()
    session.close()
    temps=list(np.ravel(temp_results))
    return jsonify(temps)



@app.route("/api/v1.0/<start>")
def tobs_date(start):
    session=Session(engine)
    results=session.query(measurement.date,func.min(measurement.tobs),func.max(measurement.tobs),func.avg(measurement.tobs))\
        .filter(measurement.date==start).all()

    session.close()
   
    start_date_temps=[]
    for minimum, maximum, average in results:
        start_temp_dict={}
        start_temp_dict["min"]= minimum
        start_temp_dict["max"]= maximum
        start_temp_dict["avg"]= average 
        start_date_temps.append(start_temp_dict)

    return jsonify(start_date_temps)


#@app.route("/api/v1.0/<start>/<end>")
#def tobs_se_date()

if __name__ == "__main__":
    app.run(debug=True)
