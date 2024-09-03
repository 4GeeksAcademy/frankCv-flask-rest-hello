from flask_sqlalchemy import SQLAlchemy


db = SQLAlchemy()
   
class User(db.Model):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True)
    user_name = db.Column(db.String(50), nullable=False)
    password = db.Column(db.String(50))
    name = db.Column(db.String(50), nullable=False)
    last_name = db.Column(db.String(50))
    email = db.Column(db.String(50),nullable=False)
    phone = db.Column(db.Integer,nullable=False) 
    like = db.relationship('Like',backref='user',lazy=True)

    def __repr__(self):
        return '<User %r>' % self.id

    def serialize(self):
        return {
            "id": self.id,
            "user_name": self.user_name,
            "name": self.name,
            "last_name": self.last_name,
            "email": self.email,
            "phone": self.phone,

            # do not serialize the password, its a security breach
        }

class Planet(db.Model):
    __tablename__ = 'planet'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    climate = db.Column(db.String(50),nullable=False)
    terrain = db.Column(db.String(50),nullable=False)
    population = db.Column(db.Integer,nullable=False)
    gravity = db.Column(db.String(50),nullable=False)
    rotation_period = db.Column(db.Integer,nullable=False)
    orbital_period= db.Column(db.Integer,nullable=False)
    diameter = db.Column(db.Integer, nullable=False)
    surface_water = db.Column(db.Integer, nullable=False) 
    character = db.relationship('Character', backref='planet',lazy=True)
    like = db.relationship('Like', backref='planet',lazy=True)

    def __repr__(self):
        return '<Planet %r>' % self.id

    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            "climate": self.climate,
            "terrain": self.terrain,
            "population": self.population,
            "gravity": self.gravity,
            "rotation_period": self.rotation_period,
            "orbital_period": self.orbital_period,
            "diameter": self.diameter,
            "surface_water": self.surface_water,         
            # do not serialize the password, its a security breach
        }

class Vehicle(db.Model):
    __tablename__ = 'vehicle'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    model = db.Column(db.String(50), nullable=False)
    manufacturer = db.Column(db.String(50), nullable=False)
    cost_in_credits = db.Column(db.Integer, nullable=False)
    length = db.Column(db.Integer, nullable=False)
    max_atmosphering_speed = db.Column(db.Integer, nullable=False)
    crew= db.Column(db.Integer, nullable=False)
    passenger = db.Column(db.Integer, nullable=False)
    cargo_capacity = db.Column(db.Integer, nullable=False)
    consumables = db.Column(db.String(50), nullable=False)
    vehicle_class = db.Column(db.String(50), nullable=False)
    like = db.relationship('Like', backref='vehicle',lazy=True)

    def __repr__(self):
        return '<Vehicle %r>' % self.id

    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            "model": self.model,
            "manufacturer": self.manufacturer,
            "cost_in_credits": self.cost_in_credits,
            "length": self.length,
            "max_atmosphering_speed": self.max_atmosphering_speed,
            "crew": self.crew,
            "passenger": self.passenger,
            "cargo_capacity": self.cargo_capacity,
            "consumables": self.consumables,
            "vehicle_class": self.vehicle_class
            # do not serialize the password, its a security breach
        }

class Character(db.Model):
    __tablename__ = 'character'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    height = db.Column(db.Integer, nullable=False)
    mass = db.Column(db.Integer, nullable=False)
    hair_color = db.Column(db.String(50),nullable=False)
    skin_color = db.Column(db.String(50),nullable=False)
    eye_color = db.Column(db.String(50), nullable=False)
    birth_year = db.Column(db.DateTime, nullable=False)
    gender = db.Column(db.String(50), nullable=False)
    planet_id = db.Column(db.Integer, db.ForeignKey('planet.id'))
    like = db.relationship('Like', backref='character',lazy=True)

    def __repr__(self):
        return '<User %r>' % self.id

    def serialize(self):
        return {
            "id":self.id,
            "name":self.name,
            "height":self.height,
            "mass":self.mass,
            "hair_color":self.hair_color,
            "skin_color":self.skin_color,
            "eye_color":self.eye_color,
            "birth_year":self.birth_year.isoformat(),
            "gender":self.gender,
            "planet_id":self.planet_id
            # do not serialize the password, its a security breach
        }

class Like(db.Model):
    __tablename__ = 'like'
    id = db.Column(db.Integer, primary_key=True)
    planet_id = db.Column(db.Integer, db.ForeignKey('planet.id'),nullable=True)
    character_id = db.Column(db.Integer, db.ForeignKey('character.id'),nullable=True)
    vehicle_id = db.Column(db.Integer, db.ForeignKey('vehicle.id'),nullable=True)
    user_id = db.Column(db.Integer,db.ForeignKey('user.id'),nullable=True)

    def __repr__(self):
        return '<User %r>' % self.id

    def serialize(self):
        return {
            "id":self.id,
            "planet_id":self.planet_id,
            "character_id":self.character_id,
            "vehicle_id":self.vehicle_id,
            "user_id":self.user_id,
            # do not serialize the password, its a security breach
        }