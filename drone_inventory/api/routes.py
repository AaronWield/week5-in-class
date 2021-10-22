from operator import methodcaller
from flask import Blueprint, json, request, jsonify
from drone_inventory.helpers import token_required
from drone_inventory.models import Drone, db, drone_schema, drones_schema

api = Blueprint('api', __name__, url_prefix='/api')

@api.route('/getdata')
def getdata():
    return {'some_value': 52, 'another_value': 'Coding Temple'}
    

# CRUD functionality below

# CREATE Drone Endpoint
@api.route('/drones', methods=['POST'])
@token_required
def create_drone(current_user_token):
    name = request.json['name']
    description = request.json['description']
    camera_quality = request.json['camera_quality']
    flight_time = request.json['flight_time']
    max_speed = request.json['max_speed']
    dimensions = request.json['dimensions']
    weight = request.json['weight']
    cost_of_prod = request.json['cost_of_prod']
    series = request.json['series']
    token = current_user_token.token

    print(f'TEST: {current_user_token.token}')
    drone = Drone(name,description,camera_quality,flight_time,
    max_speed,dimensions,weight,cost_of_prod,series,user_token = token)

    db.session.add(drone)
    db.session.commit()

    response = drone_schema.dump(drone)
    return jsonify(response)

# RETRIEVE routes
# Retrieve all drones associated w/ user token
@api.route('/drones', methods = ['GET'])
@token_required
def get_drones(current_user_token):
    owner = current_user_token.token
    drones = Drone.query.filter_by(user_token = owner).all()
    response = drones_schema.dump(drones)
    return jsonify(response)

# Retrieve 1 drone (by ID) associated w/ user token
@api.route('/drones/<id>', methods = ['GET'])
@token_required
def get_drone(current_user_token, id):
    drone = Drone.query.get(id)
    response = drone_schema.dump(drone)
    return jsonify(response)


# UPDATE a single Drone by ID
@api.route('/drones/<id>', methods = ['POST', 'PUT'])
@token_required
def update_drone(current_user_token, id):
    drone = Drone.query.get(id)
    print(drone)
    if drone:
        drone.name = request.json['name']
        drone.description = request.json['description']
        drone.camera_quality = request.json['camera_quality']
        drone.flight_time = request.json['flight_time']
        drone.max_speed = request.json['max_speed']
        drone.dimensions = request.json['dimensions']
        drone.weight = request.json['weight']
        drone.cost_of_prod = request.json['cost_of_prod']
        drone.series = request.json['series']
        drone.user_token = current_user_token.token
        db.session.commit()

        response = drone_schema.dump(drone)
        return jsonify(response)
    else:
        return jsonify({'Error': 'That drone does not exist.'})

# DELETE route
@api.route('/drones/<id>', methods = ['DELETE'])
@token_required
def delete_drone(current_user_token, id):
    drone = Drone.query.get(id)
    if drone:
        db.session.delete(drone)
        db.session.commit()
        return jsonify({'Success': f'Drone ID #{drone.id} has been deleted'})
    else: 
        return jsonify({'Error': 'That drone does not exist.'})
