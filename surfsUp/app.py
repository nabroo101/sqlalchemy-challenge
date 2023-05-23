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
@app.route("/")
def Welcome():
    """List of all available routes:"""
    return (
        f"Available Routes:<br>"
        f"/api/v1.0/precipitation<br>"
        f"/api/v1.0/stations"
        )

@app.route("/api/v1.0/precipitation")
def Precipitation():
    session = Session(engine)

    recent_date = session.query(func.max(Measurement.date)).scalar()
    year , month, day = map(int, recent_date.split('-'))
    one_year_back = date(year, month, day) - timedelta(days = 365)
    one_year_back



# Perform a query to retrieve the date and precipitation scores
    data_one_year_back = session.query(Measurement.date , Measurement.prcp).\
    filter(Measurement.date >= one_year_back).all()

    data_one_year_back_dict= dict(data_one_year_back)
    return jsonify(data_one_year_back_dict)



if __name__ =="__main__":
    app.run(debug = True)