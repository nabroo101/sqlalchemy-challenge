# Import the dependencies.
import numpy as np

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine , func
from datetime import date , timedelta

from flask import Flask , jsonify
#################################################
# Database Setup
#################################################

engine = create_engine("sqlite:///Resources/hawaii.sqlite")

# reflect an existing database into a new model
Base = automap_base()
# reflect the tables

Base.prepare(autoload_with=engine)
Base.classes.keys()
# Save references to each table
Station = Base.classes.station
Measurement = Base.classes.measurement

# Create our session (link) from Python to the DB
session = Session(engine)

#################################################
# Flask Setup
#################################################
app = Flask(__name__)


#################################################
# Flask Routes
#################################################

#setting up welcome route, with all availalbe routes displayed
@app.route("/")
def Welcome():
    """List of all available routes:"""
    return (
        f"Available Routes:<br>"
        f"/api/v1.0/precipitation<br>"
        f"/api/v1.0/stations<br>"
        f"/api/v1.0/tobs<br>"
        f"/api/v1.0/start_date<br>"
        f"/api/v1.0/start_date/end_date"
        )

#setting up the precipitaion route 
@app.route("/api/v1.0/precipitation")
def Precipitation():
    session = Session(engine)
#defining the recent date to be the most recent date in the query
    recent_date = session.query(func.max(Measurement.date)).scalar()
    year , month, day = map(int, recent_date.split('-'))
    one_year_back = date(year, month, day) - timedelta(days = 365)
    one_year_back



# Perform a query to retrieve the date and precipitation scores
    data_one_year_back = session.query(Measurement.date , Measurement.prcp).\
    filter(Measurement.date >= one_year_back).all()

    data_one_year_back_dict= dict(data_one_year_back)
    return jsonify(data_one_year_back_dict)

@app.route("/api/v1.0/stations")
def Stations():
    session = Session(engine)
    list_stations = session.query(Station.station , Station.name)
    list_stations_dict = dict(list_stations)

    return jsonify(list_stations_dict)

@app.route("/api/v1.0/tobs")
def Tobs():
    recent_date = session.query(func.max(Measurement.date)).scalar()
    year , month, day = map(int, recent_date.split('-'))

    one_year_back = date(year, month, day) - timedelta(days = 365)

    most_active_stations= session.query(Measurement.station,\
                     func.count(Measurement.station)).\
                     group_by(Measurement.station).\
                     order_by(func.count(Measurement.station).desc())
    
    most_active_station = list(most_active_stations)
    most_active_station= most_active_station[0][0]
    
    most_active_station_last12 =session.query(Measurement.date ,Measurement.tobs).\
        filter(Measurement.station == most_active_station ,\
                Measurement.date >= one_year_back )
    
# converting the list of tubles with a dict , dates are keys and temp are values
    most_active_station_last12_dict = dict(most_active_station_last12)
# returning json format
    return jsonify(most_active_station_last12_dict)

@app.route("/api/v1.0/start_date/<start_date>")
def Stat_temp(start_date):
#we can change the date 
    
    normalize = start_date.replace("/" , "-").replace(" ","")

    # recent_date = session.query(func.max(Measurement.date)).scalar()
    # year , month, day = map(int, recent_date.split('-'))
    # one_year = date(year , month , day) - sta

    stat_temp_min = session.query(Measurement.date ,func.min(Measurement.tobs)).filter(Measurement.date >= start_date)
    stat_temp_min_dict = dict(stat_temp_min)
    
    stat_temp_avg = session.query(Measurement.date ,func.min(Measurement.tobs)).filter(Measurement.date >= start_date)
    stat_temp_avg_dict = dict(stat_temp_avg)

    stat_temp_max = session.query(Measurement.date ,func.min(Measurement.tobs)).filter(Measurement.date >= start_date)
    stat_temp_max_dict = dict(stat_temp_max)

    return f"for the provided date: {start_date} <br> {stat_temp_min_dict} lowest temperature <br> {stat_temp_avg_dict} average temperature <br> {stat_temp_max_dict} highest temperature"

@app.route("/api/v1.0/start_date/end_date/<start_date>/<end_date>")
def Stat_temp_st_en(start_date , end_date):

    normalize_start = start_date.replace("/" , "-").replace(" ", "-")
    normalize_end = end_date.replace("/", "-").replace(" ", "-")

    start_end_min = session.query(func.min(Measurement.tobs)).filter(Measurement.date >= start_date).filter(Measurement.date <= end_date)
    # start_end_min_dict = dict(start_end_min)


    start_end_avg = session.query( func.avg(Measurement.tobs)).filter(Measurement.date >= start_date).filter(Measurement.date <= end_date) 
    # start_end_avg_dict = {start_end_avg.all()[0][0] : round(start_end_avg.all()[0][1] , 2)} 

    start_end_max = session.query(func.max(Measurement.tobs)).filter(Measurement.date >= start_date).filter(Measurement.date <= end_date)
    # start_end_max_dic = dict(start_end_max)
    
    return jsonify([{"min" : start_end_min.all()[0][0],"average": round(start_end_avg.all()[0][0], 2), "max": start_end_max.all()[0][0] }])
    # return f"{start_end_min_dict} lowest temperature <br> {start_end_avg_dict} average temperture <br> {start_end_max_dic} highest temreture" 


if __name__ =="__main__":
    app.run(debug = True)