from flask import Blueprint, request, jsonify
from divvy.helpers import token_required
from divvy.models import db, Trip, trip_schema, trips_schema
import urllib.request, json

api = Blueprint('api', __name__, url_prefix='/api')

@api.route('/getdata')
@token_required
def getdata():
    return {'trip_id', 'from_station_name', 'to_station_name', 'trip_duration'}

#Create
@api.route('/trip', methods = ['POST'])
@token_required
def create_trip():
    trip_id = request.json['trip_id']
    start_time = request.json['start_time']
    stop_time = request.json['stop_time']
    bikeid = request.json['bikeid']
    from_station_id = request.json['from_station_id']
    from_station_name = request.json['from_station_name']
    to_station_id = request.json['to_station_id']
    to_station_name = request.json['to_station_name']
    usertype = request.json['usertype']
    gender = request.json['gender']
    birthday = request.json['birthday']
    trip_duration = request.json['trip_duration']
    # user_token = current_user_token.token

    # print(f"User Token: {current_user_token.token}")

    trip = Trip(trip_id, start_time, stop_time, bikeid, from_station_id, from_station_name, to_station_id, to_station_name, usertype, gender, birthday, trip_duration)

    db.session.add(trip)
    db.session.commit()

    response = trip_schema.dump(trip)

    return jsonify(response)

#retrieve single
@api.route('/trip/<trip_id>', methods= ['GET'])
@token_required
def get_trip(trip_id):
    # owner = current_user_token.token
    # if owner == current_user_token.token:
    trip = Trip.query.get(trip_id)
    response = trip_schema.dump(trip)
    return jsonify(response)
    # else:
    #     return jsonify({'message': 'Valid Token Required'}), 401

#retrieve all
@api.route('/trips', methods = ['GET'])
@token_required
def get_trips():
    # owner = current_user_token.token
    trips = Trip.query.filter_by().all()
    response = trips_schema.dump(trips)
    return jsonify(response)

#Update
@api.route('/trip/<id>', methods = ['POST', 'PUT'])
@token_required
def update_trip(trip_id):
    trip = Trip.query.get(trip_id)
    # trip.trip_id = request.json['trip_id']
    trip.start_time = request.json['start_time']
    trip.stop_time = request.json['stop_time']
    trip.bikeid = request.json['bikeid']
    trip.from_station_id = request.json['from_station_id']
    trip.from_station_name = request.json['from_station_name']
    trip.to_station_id = request.json['to_station_id']
    trip.to_station_name = request.json['to_station_name']
    trip.usertype = request.json['usertype']
    trip.gender = request.json['gender']
    trip.birthday = request.json['birthday']
    trip.trip_duration = request.json['trip_duration']
    # trip.user_token = current_user_token.token

    db.session.commit()
    response = trip_schema.dump(trip)
    return jsonify(response)

#Delete
@api.route('/trip/<id>', methods = ['DELETE'])
@token_required
def delete_trip( trip_id):
    trip = Trip.query.get(trip_id)
    db.session.delete(trip)
    db.session.commit()
    response = trip_schema.dump(trip)
    return jsonify(response)
