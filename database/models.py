import os
from sqlalchemy import Column, String, Integer, DateTime
from flask_sqlalchemy import SQLAlchemy
import json

database_path = os.environ['DATABASE_URL']

db = SQLAlchemy()


def setup_db(app):
    app.config["SQLALCHEMY_DATABASE_URI"] = database_path
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    db.app = app
    db.init_app(app)
    db.create_all()


class Movie(db.Model):
    id = Column(Integer().with_variant(Integer, "sqlite"), primary_key=True)
    title = Column(String(180), nullable=False)
    release = Column(DateTime(), nullable=False)

    def json(self):
        return {
            'id': self.id,
            'title': self.title,
            'release': self.release
        }

    def insert(self):
        db.session.add(self)
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def update(self):
        db.session.commit()

    def __repr__(self):
        return json.dumps(self.json())


class Actor(db.Model):
    id = Column(Integer().with_variant(Integer, "sqlite"), primary_key=True)
    name = Column(String(80), nullable=False)
    age = Column(Integer(), nullable=False)
    sex = Column(String(80), nullable=False)

    def json(self):
        return {
            'id': self.id,
            'name': self.name,
            'age': self.age,
            'sex': self.sex
        }

    def insert(self):
        db.session.add(self)
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def update(self):
        db.session.commit()

    def __repr__(self):
        return json.dumps(self.json())
