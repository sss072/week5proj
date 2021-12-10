from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from datetime import datetime
import uuid
from sqlalchemy.orm import backref
from werkzeug.security import generate_password_hash, check_password_hash
import secrets
from flask_login import LoginManager, UserMixin
from flask_marshmallow import Marshmallow


db = SQLAlchemy()
login_manager = LoginManager()
ma = Marshmallow()


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)


class User(db.Model, UserMixin):
    id = db.Column(db.String, primary_key = True)
    name = db.Column(db.String(70), unique=True, nullable=False)
    email = db.Column(db.String(80), nullable = False)
    password = db.Column(db.String, nullable = False)
    token = db.Column(db.String, nullable = False)
    date_created = db.Column(db.DateTime, default = datetime.utcnow)
    person = db.relationship('Person', backref='owner', lazy = True)

    def __init__(self, email, password, token = '', id = ''):
        self.id = self.set_id()
        self.email = email
        self.password = self.set_password(password)
        self.token = self.get_token(24) 

    def set_id(self):
        return str(uuid.uuid4())

    def set_password(self, password):
        self.pw_hash = generate_password_hash(password)
        return self.pw_hash
    
    def get_token(self, length):
        return secrets.token_hex(length)


class Person(db.Model):
    id = db.Column(db.String, primary_key = True)
    name = db.Column(db.String(150), nullable = False)
    description = db.Column(db.String(100), nullable = True)
    date_created = db.Column(db.DateTime, nullable = False, default = datetime.utcnow)
    owner = db.Column(db.String, db.ForeignKey('user.token'), nullable = False)

    def __init__(self, name, description, date_created, owner):
        self.name = name
        self.description = description
        self.date_created = date_created
        self.owner = owner

    def set_id(self):
        return (secrets.token_urlsafe())

class PersonSchema(ma.Schema):
    class Meta:
        fields = ['id', 'name', 'description', 'date_created', 'owner']

person_schema = PersonSchema()
persons_schema = PersonSchema(many=True)