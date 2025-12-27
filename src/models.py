from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import String, Boolean, Integer, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from datetime import date

db = SQLAlchemy()


class User(db.Model):
    __tablename__ = 'user'
    id: Mapped[int] = mapped_column(primary_key=True)
    username: Mapped[str] = mapped_column( String(120), unique=True, nullable=False)
    firstname: Mapped[str] = mapped_column(String(30), nullable=False)
    lastname: Mapped[str] = mapped_column(String(30), nullable=False)
    birthdate: Mapped[date] = mapped_column(nullable=False)
    email: Mapped[str] = mapped_column( String(120), unique=True, nullable=False)
    password: Mapped[str] = mapped_column(nullable=False)
    is_active: Mapped[bool] = mapped_column(Boolean(), nullable=False)
    favoritec: Mapped[list['FavoriteCharacter']] = relationship(back_populates='user')
    favoritep: Mapped[list['FavoritePlanet'] ] = relationship(back_populates='user')
    favoritev: Mapped[list['FavoriteVehicle'] ] = relationship(back_populates='user')


    def __repr__(self):
        return f' {self.username} - {self.firstname} {self.lastname} ' 
    def serialize(self):     
        return {
            "id": self.id,
            "username": self.username,
            "firstname": self.firstname,
            "lastname": self.lastname,
            "birthdate": self.birthdate.strftime("%Y-%m-%d"),
            "email": self.email,
            "is_active": self.is_active,
            "favorite_characters": [fav.character.serialize() for fav in self.favoritec],
            "favorite_planets": [fav.planet.serialize() for fav in self.favoritep],
            "favorite_vehicles": [fav.vehicle.serialize() for fav in self.favoritev]

        }    


class Character(db.Model):
    __tablename__ = 'character'
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(100), nullable=False)
    birth_year: Mapped[str] = mapped_column(String(20), nullable=False)
    eye_color: Mapped[str] = mapped_column(String(20), nullable=False)
    gender: Mapped[str] = mapped_column(String(20), nullable=False)
    hair_color: Mapped[str] = mapped_column(String(20), nullable=False)
    skin_color: Mapped[str] = mapped_column(String(20), nullable=False)
    height: Mapped[int] = mapped_column(Integer, nullable=False)
    mass: Mapped[int] = mapped_column(Integer, nullable=False)
    favorites_by: Mapped[list['FavoriteCharacter'] ] = relationship(back_populates='character')

    def __repr__(self):
        return f' {self.name} '
    def serialize(self): 
        return {
            "id": self.id,
            "name": self.name,
            "birth year": self.birth_year,
            "eye color": self.eye_color,    
            "gender": self.gender,
            "hair color": self.hair_color,
            "skincolor": self.skin_color,
            "height": self.height,
            "mass": self.mass,
     
        }   

class Planet(db.Model):
    __tablename__ = 'planet'
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(100), nullable=False)
    climate: Mapped[str] = mapped_column(String(50), nullable=False)
    terrain: Mapped[str] = mapped_column(String(50), nullable=False)
    gravity: Mapped[str] = mapped_column(String(20), nullable=False)
    diameter: Mapped[str] = mapped_column(String(20), nullable=False)
    orbital_period: Mapped[str] = mapped_column(String(20), nullable=False)
    rotation_period: Mapped[str] = mapped_column(String(20), nullable=False)
    population: Mapped[str] = mapped_column(String(30), nullable=False)
    surface_water: Mapped[str] = mapped_column(String(20), nullable=False)
    favorites_by: Mapped[list['FavoritePlanet']] = relationship(back_populates='planet')
    
    def __repr__(self):
        return f' {self.name} '
    def serialize(self): 
        return {
            "id": self.id,
            "name": self.name,
            "climate": self.climate,
            "terrain": self.terrain,
            "gravity": self.gravity,
            "diameter": self.diameter,
            "orbital_period": self.orbital_period,
            "rotation_period": self.rotation_period,
            "population": self.population,
            "surface_water": self.surface_water,

        }   

class Vehicle(db.Model):
    __tablename__ = 'vehicle'
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(100), nullable=False)
    model: Mapped[str] = mapped_column(String(100), nullable=False)
    vehicle_class: Mapped[str] = mapped_column(String(50), nullable=False)
    manufacturer: Mapped[str] = mapped_column(String(100), nullable=False)
    cost_in_credits: Mapped[str] = mapped_column(String(20), nullable=False)
    length: Mapped[str] = mapped_column(String(20), nullable=False)
    crew: Mapped[str] = mapped_column(String(20), nullable=False)
    passengers: Mapped[str] = mapped_column(String(20), nullable=False)
    max_atmosphering_speed: Mapped[str] = mapped_column( String(20), nullable=False)
    cargo_capacity: Mapped[str] = mapped_column(String(20), nullable=False)
    consumables: Mapped[str] = mapped_column(String(50), nullable=False)
    favorites_by: Mapped[list['FavoriteVehicle']] = relationship(back_populates='vehicle')
  
    def __repr__(self):
        return f' {self.name} '
    def serialize(self): 
        return {
            "id": self.id,
            "name": self.name,
            "model": self.model,
            "vehicle_class": self.vehicle_class,
            "manufacturer": self.manufacturer,
            "cost_in_credits": self.cost_in_credits,
            "length": self.length,
            "crew": self.crew,
            "passengers": self.passengers,
            "max_atmosphering_speed": self.max_atmosphering_speed,
            "cargo_capacity": self.cargo_capacity,
            "consumables": self.consumables,
       
        }
         
class FavoriteCharacter(db.Model):
        __tablename__ = 'favoritecharacter'
        id: Mapped[int] = mapped_column(primary_key=True)
        user_id: Mapped[int] = mapped_column(ForeignKey('user.id'), nullable=False)
        character_id: Mapped[int] = mapped_column(ForeignKey('character.id'), nullable=False)
        user: Mapped['User'] = relationship(back_populates='favoritec')
        character: Mapped['Character'] = relationship( back_populates='favorites_by')

        def __repr__(self):
            return f'{self.character.name}'
        

class FavoritePlanet(db.Model):
        __tablename__ = 'favoriteplanet'
        id: Mapped[int] = mapped_column(primary_key=True)
        user_id: Mapped[int] = mapped_column(ForeignKey('user.id'))
        planet_id: Mapped[int] = mapped_column(ForeignKey('planet.id'))
        user: Mapped['User'] = relationship(back_populates='favoritep')
        planet: Mapped['Planet'] = relationship(back_populates='favorites_by')
        def __repr__(self):
            return f' {self.planet.name} '

class FavoriteVehicle(db.Model):
        __tablename__ = 'favoritevehicle'
        id: Mapped[int] = mapped_column(primary_key=True)
        user_id: Mapped[int] = mapped_column(ForeignKey('user.id'))
        vehicle_id: Mapped[int] = mapped_column(ForeignKey('vehicle.id'))
        user: Mapped['User'] = relationship(back_populates='favoritev')
        vehicle: Mapped['Vehicle'] = relationship(back_populates='favorites_by')
        def __repr__(self):
            return f' {self.vehicle.name} ' 

