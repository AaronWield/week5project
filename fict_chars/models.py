from enum import unique
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from datetime import datetime
import uuid
from werkzeug.security import generate_password_hash, check_password_hash
import secrets
from flask_login import LoginManager, UserMixin
from flask_marshmallow import Marshmallow

db = SQLAlchemy()
ma = Marshmallow()
login_manager = LoginManager()

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)

class User(db.Model, UserMixin):
    id = db.Column(db.String, primary_key = True)
    email = db.Column(db.String(150), nullable = False)
    password = db.Column(db.String, nullable = False)
    token = db.Column(db.String, unique = True)
    date_created = db.Column(db.DateTime, nullable = False, default = datetime.utcnow)
    char = db.relationship('Char', backref='owner', lazy=True)

    def __init__(self, email, password, token = '', id = ''):
        self.id = self.set_id()
        self.email = email
        self.password = self.set_password(password)
        self.token = self.set_token(24)

    def set_id(self):
        return str(uuid.uuid4())

    def set_password(self, password):
        self.pw_hash = generate_password_hash(password)
        return self.pw_hash

    def set_token(self, length):
        return secrets.token_hex(length)

class Char(db.Model):
    id = db.Column(db.String, primary_key = True)
    name = db.Column(db.String(150))
    description = db.Column(db.String(200), nullable = True)
    bio = db.Column(db.String(250))
    physical_appearance = db.Column(db.String(150), nullable = True)
    universe = db.Column(db.String(100))
    user_token = db.Column(db.String, db.ForeignKey('user.token'), nullable = False)

    def __init__(self, name, description, bio, physical_appearance, universe, user_token, id = ''):
        self.id = self.set_id()
        self.name = name
        self.description = description
        self.bio = bio
        self.physical_appearance = physical_appearance
        self.universe = universe
        self.user_token = user_token

    def set_id(self):
        return (secrets.token_urlsafe())

class CharSchema(ma.Schema):
    class Meta:
        fields = ['id', 'name','description', 'bio', 'physical_appearance', 'universe']

char_schema = CharSchema()
chars_schema = CharSchema(many=True)
