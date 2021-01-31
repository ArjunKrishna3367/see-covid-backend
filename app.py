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
cityData = db.cityData

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
    nearby_data = {}
    all_data = {}
    nearbyCodes = []
    zipCode = 10001
    query_parameters = request.args

    lat = query_parameters.get('lat')
    lon = query_parameters.get('lon')
    zipCode = query_parameters.get('zipCode')

    print(lat != None, lon != None)

    if (lat != None and lon != None):
        nearby = get_zip(float(lat), float(lon))
        nearbyCodes = nearby["nearbyZipCodes"]
        print(nearbyCodes)
        filter = {"zipCode": {"$in": [int(zipCode) for zipCode in nearbyCodes]}}
        for zipCodeData in dataDB.find(filter):
            nearby_data[zipCodeData["zipCode"]] = zipCodeData
        all_data["nearbyZipCodes"] = nearby_data
        zipCode = int(nearby["zipCode"])

    elif (zipCode != None and int(zipCode) > 10000):
        zipCode = int(zipCode)
    else:
        print("hello")
        return {}

    filter = {"zipCode": zipCode}
    for zipCodeData in dataDB.find(filter):
        all_data["zipCode"] = zipCodeData
    
    return dumps(all_data)

@app.route('/city_data', methods=['GET'])
def city_data():
    return dumps(cityData.find_one())
    
if __name__ == "__main__":
    app.run()
