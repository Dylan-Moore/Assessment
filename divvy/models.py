from email.mime import image
from tokenize import Name
from unicodedata import name
from flask_sqlalchemy import SQLAlchemy
import urllib.request
from PIL import Image
from flask_migrate import Migrate
import uuid
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
import secrets
from flask_login import UserMixin, LoginManager
from flask_marshmallow import Marshmallow

db = SQLAlchemy()
login_manager = LoginManager()
ma = Marshmallow()

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)

class User(db.Model, UserMixin):
    id = db.Column(db.String, primary_key = True)
    first_name = db.Column(db.String(150), nullable = True, default = '')
    last_name = db.Column(db.String(150), nullable = True, default='')
    username = db.Column(db.String(150), nullable = True, default = '')
    email = db.Column(db.String(150), nullable = True, default = '')
    password = db.Column(db.String(150), nullable = True, default = '')
    g_auth_verify = db.Column(db.Boolean, default = False)
    token = db.Column(db.String, default='', unique = True)
    date_create = db.Column(db.DateTime, nullable = False, default = datetime.utcnow)

    def __init__(self, email, username = '', first_name = '', last_name = '', id='', password='', token = '', g_auth_verify = False):
        self.id = self.set_id()
        self.first_name = first_name
        self.last_name = last_name
        self.username = username
        self.password = self.set_password(password)
        self.email = email
        self.token = self.set_token(24)
        self.g_auth_verify = g_auth_verify

    def set_token(self, length):
        return secrets.token_hex(length)
    def set_id(self):
        return str(uuid.uuid4())
    def set_password(self, password):
        self.pw_hash=generate_password_hash(password)
        return self.pw_hash
    def __repr__(self):
        return f"User {self.email} has been added to the database"

class Trip(db.Model):
    # id = db.Column(db.String, primary_key = True)
    trip_id = db.Column(db.String, primary_key = True)
    start_time = db.Column(db.String)
    stop_time = db.Column(db.String)
    bikeid = db.Column(db.String)
    from_station_id = db.Column(db.String)
    from_station_name = db.Column(db.String(150))
    to_station_id = db.Column(db.String)
    to_station_name = db.Column(db.String(150))
    usertype = db.Column(db.String)
    gender = db.Column(db.String(150))
    birthday = db.Column(db.String())
    trip_duration = db.Column(db.String())
    # user_token = db.Column(db.String, db.ForeignKey('user.token'), nullable = True)

    def __init__(self, trip_id, start_time, stop_time, bikeid, from_station_id, from_station_name, to_station_id, to_station_name, usertype, gender, birthday, trip_duration):
        # self.id = self.set_id()
        self.trip_id = trip_id
        self.start_time = start_time
        self.stop_time = stop_time
        self.bikeid = bikeid
        self.from_station_id = from_station_id
        self.from_station_name = from_station_name
        self.to_station_id = to_station_id
        self.to_station_name = to_station_name
        self.usertype = usertype
        self.gender = gender
        self.birthday = birthday
        self.trip_duration = trip_duration
        # self.user_token = user_token

    def __repr__(self):
        return f"Trip {self.trip_id} from {self.from_station_name} to {self.to_station_name} took {self.trip_duration}"

    def set_id(self):
        return secrets.token_urlsafe()

class TripSchema(ma.Schema):
    class Meta:
        fields = ['trip_id', 'from_station_name', 'to_station_name' 'trip_duration' ]


trip_schema = TripSchema()
trips_schema = TripSchema(many=True)
