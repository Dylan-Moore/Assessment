from flask import Flask, Blueprint, request, render_template
import psycopg2

site = Blueprint('site', __name__, template_folder = 'site_templates')
try:
    conn = psycopg2.connect(database="Divvy", user="postgres", password="Dshm1234", host="localhost")
    print("connected")
except:
    print("I am unable to connect to the database")
mycursor = conn.cursor()
app = Flask(__name__)

@site.route('/')
def home():
    return render_template('home.html')
    
@site.route('/profile')
def profile(): 
    return render_template('profile.html')

@site.route('/trip')
def trip():
    mycursor.execute("SELECT * FROM trip")
    data = mycursor.fetchall()
    return render_template('trip.html', data=data)

@site.route('/index')
def index():
    return render_template('index.html')