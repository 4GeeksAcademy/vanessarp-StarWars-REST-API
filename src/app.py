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
from models import Character, FavoriteCharacter, FavoritePlanet, FavoriteVehicle, Planet, Vehicle, db, User
# from models import Person

app = Flask(__name__)
app.url_map.strict_slashes = False

db_url = os.getenv("DATABASE_URL")
if db_url is not None:
    app.config['SQLALCHEMY_DATABASE_URI'] = db_url.replace(
        "postgres://", "postgresql://")
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




@app.route('/')
def sitemap():
    return generate_sitemap(app)

# USER


@app.route('/users', methods=['POST'])
def create_user():
    body = request.get_json(silent=True)
    if body is None:
        return jsonify({"msg": "Debe enviar información"}), 400
    if 'username' not in body:
        return jsonify({"msg": "Debe enviar el nombre de usuario"}), 400
    if 'firstname' not in body:
        return jsonify({"msg": "Debe enviar el nombre"}), 400
    if 'email' not in body:
        return jsonify({"msg": "Debe enviar el correo electrónico"}), 400
    if 'password' not in body:
        return jsonify({"msg": "Debe enviar la contraseña"}), 400
    new_user = User()
    new_user.username = body['username']
    new_user.firstname = body['firstname']
    new_user.lastname = body['lastname']
    new_user.birthdate = body['birthdate']
    new_user.email = body['email']
    new_user.password = body['password']
    new_user.is_active = True

    db.session.add(new_user)
    db.session.commit()
    return jsonify({"msg": "Usuario creado exitosamente"}), 201


@app.route('/users', methods=['GET'])
def get_users():
    users = User.query.all()
    users_serialized = []
    for user in users:
        users_serialized.append(user.serialize())
    return jsonify({'data': users_serialized}), 200


@app.route('/users/<int:user_id>/favorites', methods=['GET'])
def get_user_favorites(user_id):
    user = User.query.get(user_id)
    if not user:
        return jsonify({"msg": "Usuario no existe"}), 404

    return jsonify({
        "people": [fav.character.serialize() for fav in user.favoritec],
        "planets": [fav.planet.serialize() for fav in user.favoritep],
        "vehicles": [fav.vehicle.serialize() for fav in user.favoritev]
    }), 200


@app.route('/users/<int:user_id>', methods=['DELETE'])
def delete_user(user_id):
    user = User.query.filter_by(id=user_id).first()
    if user is None:
        return jsonify({"msg": "Usuario no encontrado"}), 404

    db.session.delete(user)
    db.session.commit()
    return jsonify({"msg": "Usuario eliminado exitosamente"}), 200


# CHARACTERS

@app.route('/characters', methods=['POST'])
def add_character():  # la informacion viene en el body de la request
    body = request.get_json(silent=True)
    if body is None:
        return jsonify({"msg": "Debe enviar información"}), 400
    if 'name' not in body:
        return jsonify({"msg": "Es obligatorio el nombre del personaje"}), 400
    if 'height' not in body:
        return jsonify({"msg": "Es obligatorio  la altura del personaje"}), 400
    if 'mass' not in body:
        return jsonify({"msg": "Es obligatorio la masa del personaje"}), 400
    if 'hair_color' not in body:
        return jsonify({"msg": "Es obligatorio el color de cabello del personaje"}), 400
    if 'skin_color' not in body:
        return jsonify({"msg": "Es obligatorio el color de piel del personaje"}), 400
    if 'eye_color' not in body:
        return jsonify({"msg": "Es obligatorio el color de ojos del personaje"}), 400
    if 'birth_year' not in body:
        return jsonify({"msg": "Es obligatorio el año de nacimiento del personaje"}), 400
    if 'gender' not in body:
        return jsonify({"msg": "Es obligatorio el género del personaje"}), 400

    new_character = Character()
    new_character.name = body['name']
    new_character.height = body['height']
    new_character.mass = body['mass']
    new_character.hair_color = body['hair_color']
    new_character.skin_color = body['skin_color']
    new_character.eye_color = body['eye_color']
    new_character.birth_year = body['birth_year']
    new_character.gender = body['gender']

    db.session.add(new_character)
    db.session.commit()

    return jsonify({"msg": "Personaje agregado exitosamente"}), 201


@app.route('/people', methods=['GET'])
def get_people():
    people = Character.query.all()
    return jsonify([pe.serialize() for pe in people]), 200


@app.route('/people/<int:people_id>', methods=['GET'])
def get_person(people_id):
    person = Character.query.get(people_id)
    if not person:
        return jsonify({"msg": "Personaje no encontrado"}), 404
    return jsonify(person.serialize()), 200


@app.route('/favorite/people/<int:people_id>', methods=['POST'])
def add_favorite_person(people_id):
    user = User.query.get(1)
    person = Character.query.get(people_id)

    if not person:
        return jsonify({"msg": "Personaje no existe"}), 404

    fav = FavoriteCharacter(user_id=user.id, character_id=people_id)
    db.session.add(fav)
    db.session.commit()
    return jsonify({"msg": "Personaje agregado a favoritos"}), 201


@app.route('/favorite/people/<int:people_id>', methods=['DELETE'])
def delete_favorite_person(people_id):
    fav = FavoriteCharacter.query.filter_by(
        user_id=1, character_id=people_id).first()
    if fav is None:
        return jsonify({"msg": "Favorito no encontrado"}), 404

    db.session.delete(fav)
    db.session.commit()

    return jsonify({"msg": "Favorito eliminado"}), 200

# PLANETS


@app.route("/planets/", methods=['POST'])
def add_planet():
    body = request.get_json(silent=True)
    if body is None:
        return jsonify({"msg": "Debe enviar información"}), 400
    if 'name' not in body:
        return jsonify({"msg": "Es obligatorio el nombre del planeta"}), 400
    if 'rotation_period' not in body:
        return jsonify({"msg": "Es obligatorio el periodo de rotación del planeta"}), 400
    if 'orbital_period' not in body:
        return jsonify({"msg": "Es obligatorio el periodo orbital del planeta"}), 400
    if 'diameter' not in body:
        return jsonify({"msg": "Es obligatorio el diámetro del planeta"}), 400
    if 'climate' not in body:
        return jsonify({"msg": "Es obligatorio el clima del planeta"}), 400
    if 'gravity' not in body:
        return jsonify({"msg": "Es obligatorio la gravedad del planeta"}), 400
    if 'terrain' not in body:
        return jsonify({"msg": "Es obligatorio el terreno del planeta"}), 400
    if 'surface_water' not in body:
        return jsonify({"msg": "Es obligatorio el agua superficial del planeta"}), 400
    if 'population' not in body:
        return jsonify({"msg": "Es obligatoria la población del planeta"}), 400

    new_planet = Planet()
    new_planet.name = body['name']
    new_planet.rotation_period = body['rotation_period']
    new_planet.orbital_period = body['orbital_period']
    new_planet.diameter = body['diameter']
    new_planet.climate = body['climate']
    new_planet.gravity = body['gravity']
    new_planet.terrain = body['terrain']
    new_planet.surface_water = body['surface_water']
    new_planet.population = body['population']

    db.session.add(new_planet)
    db.session.commit()

    return jsonify({"msg": "Planeta agregado exitosamente"}), 201


@app.route('/planets', methods=['GET'])
def get_planets():
    planets = Planet.query.all()
    return jsonify([p.serialize() for p in planets]), 200


@app.route('/planets/<int:planet_id>', methods=['GET'])
def get_planet(planet_id):
    planet = Planet.query.get(planet_id)
    if not planet:
        return jsonify({"msg": "Planeta no encontrado"}), 404
    return jsonify(planet.serialize()), 200


@app.route('/favorite/planet/<int:planet_id>', methods=['POST'])
def add_favorite_planet(planet_id):
    user = User.query.get(1)
    planet = Planet.query.get(planet_id)

    if not planet:
        return jsonify({"msg": "Planeta no existe"}), 404

    fav = FavoritePlanet(user_id=user.id, planet_id=planet_id)
    db.session.add(fav)
    db.session.commit()

    return jsonify({"msg": "Planeta agregado a favoritos"}), 201


@app.route('/favorite/planet/<int:planet_id>', methods=['DELETE'])
def delete_favorite_planet(planet_id):
    fav = FavoritePlanet.query.filter_by(
        user_id=1, planet_id=planet_id).first()
    if fav is None:
        return jsonify({"msg": "Favorito no encontrado"}), 404

    db.session.delete(fav)
    db.session.commit()

    return jsonify({"msg": "Vehículo eliminado de favoritos"}), 200


# VEHICLES
@app.route('/vehicles', methods=['POST'])
def add_vehicle():
    body = request.get_json(silent=True)
    if body is None:
        return jsonify({"msg": "Debe enviar información"}), 400
    if 'name' not in body:
        return jsonify({"msg": "Es obligatorio el nombre del vehículo"}), 400
    if 'model' not in body:
        return jsonify({"msg": "Es obligatorio el modelo del vehículo"}), 400
    if 'manufacturer' not in body:
        return jsonify({"msg": "Es obligatorio el fabricante del vehículo"}), 400
    if 'cost_in_credits' not in body:
        return jsonify({"msg": "Es obligatorio el costo en créditos del vehículo"}), 400
    if 'length' not in body:
        return jsonify({"msg": "Es obligatoria la longitud del vehículo"}), 400
    if 'max_atmosphering_speed' not in body:
        return jsonify({"msg": "Es obligatoria la velocidad máxima en atmósfera del vehículo"}), 400
    if 'crew' not in body:
        return jsonify({"msg": "Es obligatoria la tripulación del vehículo"}), 400
    if 'passengers' not in body:
        return jsonify({"msg": "Es obligatoria la cantidad de pasajeros del vehículo"}), 400
    if 'cargo_capacity' not in body:
        return jsonify({"msg": "Es obligatoria la capacidad de carga del vehículo"}), 400
    if 'consumables' not in body:
        return jsonify({"msg": "Es obligatorio los consumibles del vehículo"}), 400

    new_vehicle = Vehicle()
    new_vehicle.name = body['name']
    new_vehicle.model = body['model']
    new_vehicle.manufacturer = body['manufacturer']
    new_vehicle.cost_in_credits = body['cost_in_credits']
    new_vehicle.length = body['length']
    new_vehicle.max_atmosphering_speed = body['max_atmosphering_speed']
    new_vehicle.crew = body['crew']
    new_vehicle.passengers = body['passengers']
    new_vehicle.cargo_capacity = body['cargo_capacity']
    new_vehicle.consumables = body['consumables']

    db.session.add(new_vehicle)
    db.session.commit()

    return jsonify({"msg": "Vehículo agregado exitosamente"}), 201


@app.route('/vehicles/', methods=['GET'])
def get_vehicles():
    vehicles = Vehicle.query.all()
    return jsonify([v.serialize() for v in vehicles]), 200


@app.route('/vehicles/<int:vehicle_id>', methods=['GET'])
def get_vehicle(vehicle_id):
    vehicle = Vehicle.query.get(vehicle_id)
    if not vehicle:
        return jsonify({"msg": "Vehiculo no encontrado"}), 404
    return jsonify(vehicle.serialize()), 200


@app.route('/favorite/vehicle/<int:vehicle_id>', methods=['POST'])
def add_favorite_vehicle(vehicle_id):
    user = User.query.get(1)
    vehicle = Vehicle.query.get(vehicle_id)

    if not vehicle:
        return jsonify({"msg": "Vehículo no existe"}), 404

    fav = FavoriteVehicle(user_id=user.id, vehicle_id=vehicle_id)
    db.session.add(fav)
    db.session.commit()
    return jsonify({"msg": "Vehículo agregado a favoritos"}), 201


@app.route('/favorite/vehicle/<int:vehicle_id>', methods=['DELETE'])
def delete_favorite_vehicle(vehicle_id):
    fav = FavoriteVehicle.query.filter_by(
        user_id=1, vehicle_id=vehicle_id).first()
    if fav is None:
        return jsonify({"msg": "Favorito no encontrado"}), 404
    db.session.delete(fav)
    db.session.commit()
    return jsonify({"msg": "Favorito eliminado"}), 200


# this only runs if `$ python src/app.py` is executed
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=False)
