import os
from flask_admin import Admin
from models import db, User, Character, Planet, Vehicle, FavoriteCharacter, FavoritePlanet, FavoriteVehicle
from flask_admin.contrib.sqla import ModelView


class UserModelView(ModelView):
    column_auto_select_related = True
    column_list = ('id', 'username', 'firstname', 'lastname', 'birthdate', 'email','password', 'is_active', 'favoritec', 'favoritep', 'favoritev')

class CharacterModelView(ModelView):
    column_auto_select_related = True
    column_list = ('id', 'name', 'birth_year', 'eye_color', 'gender', 'hair_color', 'skin_color', 'height', 'mass', 'favorites_by')

class PlanetModelView(ModelView):
    column_auto_select_related = True
    column_list = ('id', 'name', 'climate', 'terrain', 'gravity', 'diameter', 'orbital_period', 'rotation_period', 'population', 'surface_water', 'favorites_by')   

class VehicleModelView(ModelView):
    column_auto_select_related = True
    column_list = ('id', 'name', 'model', 'vehicle_class', 'manufacturer', 'cost_in_credits', 'max_atmosphering_speed', 'cargo_capacity', 'consumables', 'favorites_by')    

class FavoriteCharacterModelView(ModelView):
    column_auto_select_related = True
    column_list = ('id',  'user', 'character')  

class FavoritePlanetModelView(ModelView):
    column_auto_select_related = True
    column_list = ('id',  'user', 'planet')    

class FavoriteVehicleModelView(ModelView):
    column_auto_select_related = True
    column_list = ('id',  'user', 'vehicle')    


def setup_admin(app):
    app.secret_key = os.environ.get('FLASK_APP_KEY', 'sample key')
    app.config['FLASK_ADMIN_SWATCH'] = 'slate' #SE CAMBIA EL TEMA A EN LA TABLA 
    admin = Admin(app, name='4Geeks Admin', template_mode='bootstrap3')

    
    # Add your models here, for example this is how we add a the User model to the admin
    admin.add_view(UserModelView(User, db.session))
    admin.add_view(CharacterModelView(Character, db.session))
    admin.add_view(PlanetModelView(Planet, db.session))
    admin.add_view(VehicleModelView(Vehicle, db.session))
    admin.add_view(FavoriteCharacterModelView(FavoriteCharacter, db.session))
    admin.add_view(FavoritePlanetModelView(FavoritePlanet, db.session))
    admin.add_view(FavoriteVehicleModelView(FavoriteVehicle, db.session))  

    # You can duplicate that line to add mew models
    # admin.add_view(ModelView(YourModelName, db.session))