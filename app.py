import flask
from flask import request
import pymongo
from bson.json_util import dumps
from flask_cors import CORS
from datetime import datetime, timedelta
import pycountry
from nearbyZipCodes import get_zip

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

@app.route('/nearby_zipCodes', methods=['GET'])
def nearby_zipCodes():
    data = []
    query_parameters = request.args
    lat = float(query_parameters.get('lat'))
    lon = float(query_parameters.get('lon'))
    return get_zip(lat, lon)

@app.route('/get_info', methods=['GET'])
def nearby_data():
    data = []
    query_parameters = request.args

    # lat = query_parameters.get('lat')
    # lon = query_parameters.get('lat')
    zipCode = query_parameters.get('zipCode')

    # if (lat != None and lon != None):
    #     nearby_data = nearby_zipCodes
    if (zipCode != None and int(zipCode) > 10000):
        filter = {"zipCode": int(zipCode)}
    else:
        return '''<h1>No zipcode provided</h1>'''
    
    for zipCodeData in dataDB.find(filter):
        data.append(zipCodeData)
    return dumps(data)
    
if __name__ == "__main__":
    app.run()
