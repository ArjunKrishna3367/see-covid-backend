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
def source_data():
    return dumps(dataDB.find_one())
    
if __name__ == "__main__":
    app.run()
