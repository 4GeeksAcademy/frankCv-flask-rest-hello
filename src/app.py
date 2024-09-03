"""
This module takes care of starting the API Server, Loading the DB and Adding the endpoints
"""
import os
from flask import Flask, request, jsonify, url_for
from flask_migrate import Migrate
from flask_swagger import swagger
from flask_cors import CORS
from utils import APIException, generate_sitemap
from admin import setup_admin
from models import db, User,Planet,Vehicle,Character,Like
#from models import Person

app = Flask(__name__)
app.url_map.strict_slashes = False

db_url = os.getenv("DATABASE_URL")
if db_url is not None:
    app.config['SQLALCHEMY_DATABASE_URI'] = db_url.replace("postgres://", "postgresql://")
else:
    app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:////tmp/test.db"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

MIGRATE = Migrate(app, db)
db.init_app(app)
CORS(app)
setup_admin(app)

# Handle/serialize errors like a JSON object
@app.errorhandler(APIException)
def handle_invalid_usage(error):
    return jsonify(error.to_dict()), error.status_code

# generate sitemap with all your endpoints
@app.route('/')
def sitemap():
    return generate_sitemap(app)
#/////////////// USER //////////////////
@app.route('/users', methods=['GET'])
def get_users():
    #consultar el modelo de todos los registros
    try:
        query_results = User.query.all()
        results = list(map(lambda item: item.serialize(),query_results))
        response_body = {
            "msg": "ok",
            "results": results
        }
        return jsonify(response_body), 200
    except Exception as e:
        return jsonify({'error':'Internal Server Error', 'message':str(e)}),500


@app.route('/users/<int:user_id>', methods=['GET'])
def get_user_id(user_id):    
    try:
        #consultar el modelo de todos los registros
        query_user = User.query.filter_by(id=user_id).first() 
        response_body = {
            "msg": "ok",
            "result": query_user.serialize()
        }
        return jsonify(response_body), 200
    except Exception as e:
        return jsonify({'error':'Internal Server Error', 'message':str(e)}),500
    
@app.route('/users',methods=['POST'])
def create_user():
    try:
        user_name = request.json.get('user_name')
        name=request.json.get('name')
        last_name=request.json.get('last_name')
        email=request.json.get('email')
        phone=request.json.get('phone')
        #Validate if request body is not empty
        if not user_name or not name or not last_name or not email or not phone:
            return jsonify({'error':'User name, name, last name, email and phone are required'}),400            
        #Validate if user and email is already taken
        existing_user = User.query.filter_by(user_name = user_name).first()
        existing_email = User.query.filter_by(email = email).first()
        if existing_user and existing_email:
            return jsonify({'error': 'email or user already exists'})
        new_user = User(user_name=user_name,name=name,last_name=last_name,email=email,phone=phone)
        db.session.add(new_user)
        db.session.commit()

        return jsonify({'message': 'User created successfully', 'user_created':new_user.serialize()}),201
    except Exception as e:
        return jsonify({'message':'Internal Server Error','error':str(e)}),500
@app.route('/users/<int:id>',methods=['PUT'])
def update_user(id):
    try:
        user = User.query.get(id)
        if not user:
            return jsonify({'error':'User not found.'}),404
        #get data from request body:
        # user_name = request.json.get('user_name')
        name = request.json.get('name')
        last_name = request.json.get('last_name')
        email=request.json.get('email')
        phone=request.json.get('phone')
        #validate if some field is emptynot user_name or
        if  not name or not last_name or not email or not phone:
            return jsonify({'error':'All fields (name , last name, email and phone) are required'}),400
        #verify if existing email or user is already taken
        if email != user.email:
            existing_email = User.query.filter_by(email=email).first()
            if existing_email:
                return jsonify({'error': 'Email is already taken '}),409
            user.email = email
        user.name = name
        user.last_name = last_name
        
        user.phone = phone
        #Save changes in database
        db.session.commit()
        return jsonify({'message':'user updated succesfully','updated_user': user.serialize()})
    except Exception as e:
        return jsonify({'message': 'Internal Server Error','error':str(e)}),500
@app.route('/users/<int:id>',methods=['DELETE'])
def delete_user(id):
    try:
        #find user
        user = User.query.get(id)
        if not user:
            return jsonify({'error':'User not found'}),404
        #delete user
        db.session.delete(user)
        db.session.commit()
        return jsonify({'message': 'User deleted successfully.'}),200
    except Exception as e:
        return jsonify({'message':"Internal Server Error","error":str(e)}),500
# #/////////////// Planet //////////////////
@app.route('/planets', methods=['GET'])
def get_planets():
    try:
        #consultar el modelo de todos los registros
        query_results = Planet.query.all()
        results = list(map(lambda item: item.serialize(),query_results))
        response_body = {
            "msg": "ok",
            "results": results
        }
        return jsonify(response_body), 200
    except Exception as e:
        return jsonify({'error': 'Internal Server Error', 'message':str(e)}),500

@app.route('/planets/<int:planet_id>', methods=['GET'])
def get_planet_id(planet_id):    
    try:
        #consultar el modelo de todos los registros
        query_planet = Planet.query.filter_by(id=planet_id).first()    
        response_body = {
            "msg": "ok",
            "result": query_planet.serialize()
        }
        return jsonify(response_body), 200
    except Exception as e:
        return jsonify({'error':'Internal Server Error','message':str(e)}),500
@app.route('/planets',methods=['POST'])
def create_planet():
    try:
        name=request.json.get('name')
        climate=request.json.get('climate')
        terrain=request.json.get('terrain')
        population=request.json.get('population')
        gravity=request.json.get('gravity')
        rotation_period=request.json.get('rotation_period')
        orbital_period=request.json.get('orbital_period')
        diameter=request.json.get('diameter')
        surface_water=request.json.get('surface_water')

        labels_values = {name,climate,terrain,population,gravity,rotation_period,orbital_period,diameter,surface_water}
        # for label in labels_values:
        #     if not label:
        #         return jsonify({'error':'All fields (name, climate, terrain, population, gravity, rotation_period, orbital_period, diameter, surface_water) are required'}),400
        if not name or not climate or not terrain or not population or not gravity or not rotation_period or not orbital_period or not diameter or not surface_water:
            return jsonify({'error':'All fields (name, climate, terrain, population, gravity, rotation_period, orbital_period, diameter, surface_water) are required'}),400
        existing_planet = Planet.query.filter_by(name=name).first()
        if existing_planet:
            return jsonify({'error': 'Planet already exists'}),409
        new_planet = Planet(name=name,climate=climate,terrain=terrain, population=population, gravity=gravity, rotation_period=rotation_period, orbital_period=orbital_period, diameter=diameter, surface_water=surface_water)

        db.session.add(new_planet)
        db.session.commit()
        return jsonify({'message':'Planet created successfully','planet_created':new_planet.serialize()}),201
    except Exception as e:
        return jsonify({'message':'Internal Server Error','error':str(e)}),500
    
@app.route('/planets/<int:id>',methods=['PUT'])
def update_planet(id):
    try:
        planet = Planet.query.get(id)
        if not planet:
            return jsonify({'error':'Planet not found.'}),404
        #Retrieve data from body request
        name=request.json.get('name')
        climate=request.json.get('climate')
        terrain=request.json.get('terrain')
        population=request.json.get('population')
        gravity=request.json.get('gravity')
        rotation_period=request.json.get('rotation_period')
        orbital_period=request.json.get('orbital_period')
        diameter=request.json.get('diameter')
        surface_water=request.json.get('surface_water')

        if name != planet.name:
            existing_planet = Planet.query.filter_by(name=name).first()
            if existing_planet:
                return jsonify({'error':'Planet already exists.'}),409
            planet.name = name
        #updating rest of fields
        planet.climate= climate
        planet.terrain= terrain
        planet.population= population
        planet.gravity= gravity
        planet.rotation_period= rotation_period
        planet.orbital_period= orbital_period
        planet.diameter= diameter
        planet.surface_water= surface_water
        #saving changes in db
        db.session.commit()
        return jsonify({'messagee':'Planet updated successfully','updated_planet':planet.serialize()}),200
    except Exception as e:
        return jsonify({"message": "Internal Server Error","error":str(e)}),500

@app.route('/planets/<int:id>',methods=['DELETE'])
def delete_planet(id):
    try:
        planet = Planet.query.get(id)
        if not planet:
            return jsonify({'error':'Planet not found'}),404
        #Delete Planet
        db.session.delete(planet)
        db.session.commit()
        return jsonify({'message':'Planet deleted successfully.'}),200
    except Exception as e:
        return jsonify({"message": "Internal Server Error","error":str(e)}),500
# #/////////////// Vehicle //////////////////
@app.route('/vehicles', methods=['GET'])
def get_vehicles():
    try:
        #consultar el modelo de todos los registros
        query_results = Vehicle.query.all()
        results = list(map(lambda item: item.serialize(),query_results))
        response_body = {
            "msg": "ok",
            "results": results
        }
        return jsonify(response_body), 200
    except Exception as e:
        return jsonify({'error': 'Internal Server Error', 'message':str(e)}),500

@app.route('/vehicles/<int:vehicle_id>', methods=['GET'])
def get_vehicle_id(vehicle_id):    
    try:
        #consultar el modelo de todos los registros
        query_vehicle = Vehicle.query.filter_by(id=vehicle_id).first()    
        response_body = {
            "msg": "ok",
            "result": query_vehicle.serialize()
        }
        return jsonify(response_body), 200
    except Exception as e:
        return jsonify({'error':'Internal Server Error','message':str(e)}),500
@app.route('/vehicles',methods=['POST'])
def create_vehicle():
    try:
        name =request.json.get('name')
        model = request.json.get('model')
        manufacturer = request.json.get('manufacturer')
        cost_in_credits = request.json.get('cost_in_credits')
        length = request.json.get('length')
        max_atmosphering_speed = request.json.get('max_atmosphering_speed')
        crew = request.json.get('crew')
        passenger = request.json.get('passenger')
        cargo_capacity = request.json.get('cargo_capacity')
        consumables = request.json.get('consumables')
        vehicle_class = request.json.get('vehicle_class')

        labels_values = {name, model, manufacturer, cost_in_credits, length, max_atmosphering_speed, crew, passenger, cargo_capacity, consumables, vehicle_class}
        # for label in labels_values:
        #     if not label:
        #         return jsonify({'error':'All fields (name, climate, terrain, population, gravity, rotation_period, orbital_period, diameter, surface_water) are required'}),400
        if not name or not model or not manufacturer or not cost_in_credits or not length or not max_atmosphering_speed or not crew or not passenger or not cargo_capacity or not consumables or not vehicle_class:
            return jsonify({'error':'All fields (name, model, manufacturer, cost_in_credits, length, max_atmosphering_speed, crew, passenger, cargo_capacity, consumables, vehicle_class) are required'}),400
        existing_vehicle = Vehicle.query.filter_by(name=name).first()
        if existing_vehicle:
            return jsonify({'error': 'Vehicle already exists'}),409
        new_vehicle = Vehicle(name=name,model=model,manufacturer=manufacturer, cost_in_credits=cost_in_credits, length=length, max_atmosphering_speed=max_atmosphering_speed, crew=crew, passenger=passenger, cargo_capacity=cargo_capacity, consumables=consumables,
                        vehicle_class=vehicle_class)

        db.session.add(new_vehicle)
        db.session.commit()
        return jsonify({'message':'Planet created successfully','vehicle_created':new_vehicle.serialize()}),201
    except Exception as e:
        return jsonify({'message':'Internal Server Error','error':str(e)}),500
    
@app.route('/vehicles/<int:id>',methods=['PUT'])
def update_vehicle(id):
    try:
        vehicle = Vehicle.query.get(id)
        if not vehicle:
            return jsonify({'error':'Vehicle not found.'}),404
        #Retrieve data from body request
        name =request.json.get('name')
        model = request.json.get('model')
        manufacturer = request.json.get('manufacturer')
        cost_in_credits = request.json.get('cost_in_credits')
        length = request.json.get('length')
        max_atmosphering_speed = request.json.get('max_atmosphering_speed')
        crew = request.json.get('crew')
        passenger = request.json.get('passenger')
        cargo_capacity = request.json.get('cargo_capacity')
        consumables = request.json.get('consumables')
        vehicle_class = request.json.get('vehicle_class')

        if name != vehicle.name:
            existing_planet = Vehicle.query.filter_by(name=name).first()
            if existing_planet:
                return jsonify({'error':'Vehicle already exists.'}),409
            vehicle.name = name
        #updating rest of fields
        vehicle.model= model
        vehicle.manufacturer= manufacturer
        vehicle.cost_in_credits= cost_in_credits
        vehicle.length= length
        vehicle.max_atmosphering_speed= max_atmosphering_speed
        vehicle.crew= crew
        vehicle.passenger= passenger
        vehicle.cargo_capacity= cargo_capacity
        vehicle.consumables= consumables
        vehicle.vehicle_class= vehicle_class
        #saving changes in db
        db.session.commit()
        return jsonify({'message':'Vehicle updated successfully','updated_vehicle':vehicle.serialize()}),200
    except Exception as e:
        return jsonify({"message": "Internal Server Error","error":str(e)}),500

@app.route('/vehicles/<int:id>',methods=['DELETE'])
def delete_vehicle(id):
    try:
        vehicle = Vehicle.query.get(id)
        if not vehicle:
            return jsonify({'error':'Vehicle not found'}),404
        #Delete Vehicle
        db.session.delete(vehicle)
        db.session.commit()
        return jsonify({'message':'Vehicle deleted successfully.'}),200
    except Exception as e:
        return jsonify({"message": "Internal Server Error","error":str(e)}),500
# #/////////////// Characters //////////////////
@app.route('/characters', methods=['GET'])
def get_characters():
    try:
        #consultar el modelo de todos los registros
        query_results = Character.query.all()
        results = list(map(lambda item: item.serialize(),query_results))
        response_body = {
            "msg": "ok",
            "results": results
        }
        return jsonify(response_body), 200
    except Exception as e:
        return jsonify({'message':'Internal Server Error', 'error': str(e)}),500

@app.route('/characters/<int:character_id>', methods=['GET'])
def get_character_id(character_id):    
    try:
        #consultar el modelo de todos los registros
        query_character = Character.query.filter_by(id=character_id).first()    
        response_body = {
            "msg": "ok",
            "result": query_character.serialize()
        }
        return jsonify(response_body), 200
    except Exception as e:
        return jsonify({'message':'Internal Server Error','error':str(e)}),500
@app.route('/characters',methods=['POST'])
def create_character():
    try: 
        name = request.json.get('name')
        height = request.json.get('height')
        mass = request.json.get('mass')
        hair_color = request.json.get('hair_color')
        skin_color = request.json.get('skin_color')
        eye_color = request.json.get('eye_color')
        birth_year = request.json.get('birth_year')
        gender = request.json.get('gender')
        planet_id = request.json.get('planet_id')

        labels_values = {name, height, mass, hair_color, skin_color, eye_color, birth_year, gender, planet_id}
        # for label in labels_values:
        #     if not label:
        #         return jsonify({'error':'All fields (name, climate, terrain, population, gravity, rotation_period, orbital_period, diameter, surface_water) are required'}),400
        if not name or not height or not mass or not  hair_color or not skin_color or not eye_color or not birth_year or not gender or not planet_id:
            return jsonify({'error':'All fields (name, height, mass, hair_color, skin_color, eye_color, birth_year, gender, planet_id) are required'}),400
        existing_character = Character.query.filter_by(name=name).first()
        existing_planet = Planet.query.filter_by(id=planet_id)
        if existing_character:
            return jsonify({'error': 'Vehicle already exists'}),409
        if existing_planet :
            return jsonify({'error':'Planet not found'}),404
        new_character = Character(name, height, mass,hair_color,skin_color,eye_color,birth_year,gender,planet_id)

        db.session.add(new_character)
        db.session.commit()
        return jsonify({'message':'Character created successfully','character_created':new_character.serialize()}),201
    except Exception as e:
        return jsonify({'message':'Internal Server Error','error':str(e)}),500
    
@app.route('/characters/<int:id>',methods=['PUT'])
def update_character(id):
    try:
        character = Character.query.get(id)
        if not character:
            return jsonify({'error':'Character not found.'}),404
        #Retrieve data from body request
        name = request.json.get('name')
        height = request.json.get('height')
        mass = request.json.get('mass')
        hair_color = request.json.get('hair_color')
        skin_color = request.json.get('skin_color')
        eye_color = request.json.get('eye_color')
        birth_year = request.json.get('birth_year')
        gender = request.json.get('gender')
        planet_id = request.json.get('planet_id')
        if name != character.name:
            existing_character = Character.query.filter_by(name=name).first()
            existing_planet_id = Planet.query.filter_by(id=id).first()
            if existing_character:
                return jsonify({'error':'Character already exists.'}),409
            if not existing_planet_id:
                return jsonify({'error':'Planet id not found'}),404
            character.name = name
        #updating rest of fields
        character.name = name
        character.height = height
        character.mass = mass
        character.hair_color = hair_color
        character.skin_color = skin_color
        character.eye_color = eye_color
        character.birth_year = birth_year
        character.gender = gender
        character.planet_id = 'https://didactic-space-fishstick-5p9wpwp99xq3v4p4-3000.app.github.dev/planets/'+planet_id
        #saving changes in db
        db.session.commit()
        return jsonify({'message':'Character updated successfully','updated_character':character.serialize()}),200
    except Exception as e:
        return jsonify({"message": "Internal Server Error","error":str(e)}),500

@app.route('/characters/<int:id>',methods=['DELETE'])
def delete_character(id):
    try:
        character = Character.query.get(id)
        if not character:
            return jsonify({'error':'Character not found'}),404
        #Delete Vehicle
        db.session.delete(character)
        db.session.commit()
        return jsonify({'message':'Character deleted successfully.'}),200
    except Exception as e:
        return jsonify({"message": "Internal Server Error","error":str(e)}),500
# #/////////////// Like //////////////////
@app.route('/likes', methods=['GET'])
def get_likes():
    try:
        #consultar el modelo de todos los registros
        query_results = Like.query.all()
        results = list(map(lambda item: item.serialize(),query_results))
        response_body = {
            "msg": "ok",
            "results": results
        }
        return jsonify(response_body), 200
    except Exception as e:
        return jsonify({'message':'Internal Server Error','error':str(e)}),500

@app.route('/likes/<int:like_id>', methods=['GET'])
def get_like_id(like_id):    
    try:
        #consultar el modelo de todos los registros
        query_like = Like.query.filter_by(id=like_id).first()    
        response_body = {
            "msg": "ok",
            "result": query_like.serialize()
        }
        return jsonify(response_body), 200
    except Exception as e:
        return jsonify({'message':'Internal Server Error','error':str(e)}),500

@app.route('/likes',methods=['POST'])
def create_like():
    try: 
        planet_id = request.json.get('planet_id')
        character_id = request.json.get('character_id')
        vehicle_id = request.json.get('vehicle_id')
        user_id = request.json.get('user_id')

        labels_values = {planet_id,character_id,vehicle_id,user_id}
        # for label in labels_values:
        #     if not label:
        #         return jsonify({'error':'All fields (name, climate, terrain, population, gravity, rotation_period, orbital_period, diameter, surface_water) are required'}),400
        if not planet_id and not character_id and not vehicle_id and not user_id:
            return jsonify({'error':'At least one field shoudlnt be empty'}),400
        existing_character = Character.query.filter_by(id=character_id).first()
        existing_planet = Planet.query.filter_by(id=planet_id).first()
        existing_user = User.query.filter_by(id=user_id).first()
        existing_vehicle = Vehicle.query.filter_by(id=vehicle_id).first()
        if not existing_character:
            return jsonify({'error': 'Character not found'}),404
        if not existing_planet :
            return jsonify({'error':'Planet not found'}),404
        if not existing_user :
            return jsonify({'error':'User not found'}),404
        if not existing_vehicle :
            return jsonify({'error':'Vehicle not found'}),404
        new_like = Like(planet_id,character_id,vehicle_id,user_id)

        db.session.add(new_like)
        db.session.commit()
        return jsonify({'message':'Like created successfully','like_created':new_like.serialize()}),201
    except Exception as e:
        return jsonify({'message':'Internal Server Error','error':str(e)}),500
    
@app.route('/likes/<int:id>',methods=['PUT'])
def update_like(id):
    try:
        like = Like.query.get(id)
        if not like:
            return jsonify({'error':'Character not found.'}),404
        #Retrieve data from body request
        planet_id = request.json.get('planet_id')
        character_id = request.json.get('character_id')
        vehicle_id = request.json.get('vehicle_id')
        user_id = request.json.get('user_id')
        existing_character = Character.query.filter_by(id=character_id).first()
        existing_planet = Planet.query.filter_by(id=planet_id).first()
        existing_user = User.query.filter_by(id=user_id).first()
        existing_vehicle = Vehicle.query.filter_by(id=vehicle_id).first()
        if not existing_character:
            return jsonify({'error': 'Character not found'}),404
        if not existing_planet :
            return jsonify({'error':'Planet not found'}),404
        if not existing_user :
            return jsonify({'error':'User not found'}),404
        if not existing_vehicle :
            return jsonify({'error':'User not found'}),404
        #updating rest of fields
        like.planet_id ='https://didactic-space-fishstick-5p9wpwp99xq3v4p4-3000.app.github.dev/planets/'+ planet_id
        like.character_id ='https://didactic-space-fishstick-5p9wpwp99xq3v4p4-3000.app.github.dev/characters/'+ character_id
        like.vehicle_id ='https://didactic-space-fishstick-5p9wpwp99xq3v4p4-3000.app.github.dev/vehicles/'+ vehicle_id
        like.user_id ='https://didactic-space-fishstick-5p9wpwp99xq3v4p4-3000.app.github.dev/users/'+ user_id
        #saving changes in db
        db.session.commit()
        return jsonify({'message':'Like updated successfully','updated_like':like.serialize()}),200
    except Exception as e:
        return jsonify({"message": "Internal Server Error","error":str(e)}),500

@app.route('/likes/<int:id>',methods=['DELETE'])
def delete_like(id):
    try:
        like = Like.query.get(id)
        if not like:
            return jsonify({'error':'Like not found'}),404
        #Delete Like
        db.session.delete(like)
        db.session.commit()
        return jsonify({'message':'Like deleted successfully.'}),200
    except Exception as e:
        return jsonify({"message": "Internal Server Error","error":str(e)}),500

# this only runs if `$ python src/app.py` is executed
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=False)
