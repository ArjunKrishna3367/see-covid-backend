import flask
from flask import request
import pymongo
from bson.json_util import dumps
from flask_cors import CORS
from datetime import datetime, timedelta
import pycountry

app = flask.Flask(__name__)
CORS(app)
app.config["DEBUG"] = True
client = pymongo.MongoClient("mongodb+srv://akrishna:J3WfhZuNfkcNx9uC@coviddata.drkjr.mongodb.net/coviddata?retryWrites=true&w=majority")
db = client.test
dataDB = db.testData

@app.route('/', methods=['GET'])
def home():
    return '''<h1>Data API</h1>
<p>An API for NYC Covid Data for See Covid.</p>'''

@app.errorhandler(404)
def page_not_found(e):
    return "<h1>404</h1><p>The resource could not be found.</p>", 404

@app.route('/percent_1day', methods=['GET'])
def percent_1day():
    return dumps(dataDB.find_one())

@app.route('/get_info', methods=['GET'])
def nearby_data():
    data = []
    query_parameters = request.args
    myZipCode = query_parameters.get('zipCode')

    # nearby = nearbyZipCodes(myZipCode)
    nearby = [10001, 10002, 10003]

    filter = {"zipCode": {"$in" : [zipCode for zipCode in nearby]}}
    
    for zipCodeData in dataDB.find(filter):
        data.append(zipCodeData)
    return dumps(data)
    
if __name__ == "__main__":
    app.run()
