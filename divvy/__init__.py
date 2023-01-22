from flask import Flask, render_template, request, redirect, url_for
import os
from os.path import join, dirname, realpath
from .site.routes import site
from config import Config
from divvy.helpers import JSONEncoder
from .authentication.routes import auth
from .api.routes import api
from flask_migrate import Migrate
from .models import db as root_db, login_manager, ma
from flask_cors import CORS
import pandas as pd


app = Flask(__name__)

app.register_blueprint(site)
app.register_blueprint(auth)
app.register_blueprint(api)
app.config.from_object(Config)

root_db.init_app(app)

migrate = Migrate(app, root_db)

login_manager.init_app(app)
login_manager.login_view = 'auth.signin'

ma.init_app(app)

app.json_encoder = JSONEncoder

CORS(app)

app.config["DEBUG"] = True

#Upload folder
UPLOAD_FOLDER = 'static/files'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

#Root URL
@app.route('/')
def index():
    return render_template('uploader.html')

# Get the uploaded files
@app.route("/", methods=['POST'])
def uploadFiles():
    uploaded_file = request.files['file']
    if uploaded_file.filename != '':
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], uploaded_file.filename)
        #set the file path
        uploaded_file.save(file_path)
        #save the file
    return redirect(url_for('uploader'))

if (__name__ == "__main__"):
    app.run(port = 5000)

def parseCSV(filePath):
    #CVS Column Names
    col_names = ['trip_id', 'start_time', 'stop_time', 'bikeid', 'from_station_id', 'from_station_name', 'to_station_id', 'to_station_name', 'usertype', 'gender', 'birthday', 'trip_duration']
    #Use Pandas to parse the CSV file
    csvData = pd.read_csv(filePath, names=col_names, header=None)
    #Loop through the Rows
    for i, row in csvData.iterrows():
        print(i, row['trip_id'],row['start_time'], row['stop_time'], row['bikeid'], row['from_station_id'], row['from_station_name'], row['to_station_id'], row['to_station_name'], row['usertype'], row['gender'], row['birthday'], row['trip_duration'] )
