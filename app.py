import os
from flask import Flask, request, abort, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS

from database.models import setup_db, Movie, Actor
from auth.auth import AuthError, requires_auth

PERMISSION_GET_ACTOR = 'get:actors'
PERMISSION_CREATE_ACTOR = 'post:actors'
PERMISSION_UPDATE_ACTOR = 'patch:actors'
PERMISSION_DELETE_ACTOR = 'delete:actors'

PERMISSION_GET_MOVIE = 'get:movies'
PERMISSION_CREATE_MOVIE = 'post:movies'
PERMISSION_UPDATE_MOVIE = 'patch:movies'
PERMISSION_DELETE_MOVIE = 'delete:movies'

def create_app(test_config=None):
  app = Flask(__name__)
  CORS(app)

  return app

app = create_app()
setup_db(app)

def get_array_json(obj):
    arr = []
    for one in obj:
        arr.append(one.json())
    return arr

def get_validated_body_actor():
    name = request.get_json().get('name')
    age = request.get_json().get('age')
    sex = request.get_json().get('sex')

    if name is None or age is None or sex is None:
        abort(400, "Wrong request body.")

    return name, age, sex

def get_validated_body_movie():
    title = request.get_json().get('title')
    release = request.get_json().get('release')

    if title is None or release is None:
        abort(400, "Wrong request body.")

    return title, release

@app.route('/actors')
@requires_auth(PERMISSION_GET_ACTOR)
def get_actors():
    return jsonify({
                    "success": True,
                    "actors": get_array_json(Actor.query.all())
                    }), 200

@app.route('/movies')
@requires_auth(PERMISSION_GET_MOVIE)
def get_movies():
    return jsonify({
                    "success": True,
                    "actors": get_array_json(Movie.query.all())
                    }), 200

@app.route('/actors/<int:id>', methods=['DELETE'])
@requires_auth(PERMISSION_DELETE_ACTOR)
def delete_actor(id):
    actor = Actor.query.filter_by(id=id).one_or_none()
    if actor is None:
        abort(404, "Not Exists Actor.")
    try:
        actor.delete()
    except Exception:
        abort(500, "Internal Error")
    return jsonify({
                    "success": True,
                    "actors": get_array_json(Actor.query.all())
                    }), 200

@app.route('/movies/<int:id>', methods=['DELETE'])
@requires_auth(PERMISSION_DELETE_MOVIE)
def delete_movie(id):
    movie = Movie.query.filter_by(id=id).one_or_none()
    if movie is None:
        abort(404, "Not Exists Movie.")
    try:
        movie.delete()
    except Exception:
        abort(500, "Internal Error")
    return jsonify({
                    "success": True,
                    "actors": get_array_json(Movie.query.all())
                    }), 200

@app.route('/actors', methods=['POST'])
@requires_auth(PERMISSION_CREATE_ACTOR)
def create_actor():
    name, age, sex = get_validated_body_actor()
    try:
        actor = Actor(name=name, age=age, sex=sex)
        actor.insert()
    except Exception:
        abort(500, "Internal Error")
    return jsonify({
                    "success": True,
                    "actor": actor.json()
                    }), 200

@app.route('/movies', methods=['POST'])
@requires_auth(PERMISSION_CREATE_MOVIE)
def create_movie():
    title, release = get_validated_body_movie()
    try:
        movie = Movie(title=title, release=release)
        movie.insert()
    except Exception:
        abort(500, "Internal Error")
    return jsonify({
                    "success": True,
                    "movie": movie.json()
                    }), 200

@app.route('/actors/<int:id>', methods=['PATCH'])
@requires_auth(PERMISSION_UPDATE_ACTOR)
def update_actor(id):
    name, age, sex = get_validated_body_actor()
    actor = Actor.query.filter_by(id=id).one_or_none()
    if actor is None:
        abort(404, "Not Exists Actor.")
    try:
        actor.name = name
        actor.age = age
        actor.sex = sex
        actor.update()
    except Exception:
        abort(500, "Internal Error")
    return jsonify({
                    "success": True,
                    "actor": actor.json()
                    }), 200

@app.route('/movies/<int:id>', methods=['PATCH'])
@requires_auth(PERMISSION_UPDATE_MOVIE)
def update_movie(id):
    title, release = get_validated_body_movie()
    movie = Movie.query.filter_by(id=id).one_or_none()
    if movie is None:
        abort(404, "Not Exists Actor.")
    try:
        movie.title = title
        movie.release = release
        movie.update()
    except Exception:
        abort(500, "Internal Error")
    return jsonify({
                    "success": True,
                    "movie": movie.json()
                    }), 200

@app.route('/')
def hello():
    return 'Hi everyone :)'


## Error Handling
@app.errorhandler(400)
def bad_request(error):
    return jsonify({
                    "success": False,
                    "error": 400,
                    "message": str(error)
                    }), 400

@app.errorhandler(AuthError)
def wrong_auth(error):
    return jsonify({
                    "success": False,
                    "error": 401,
                    "message": error.to_dict().get('error')
                    }), 401

@app.errorhandler(422)
def unprocessable(error):
    return jsonify({
                    "success": False,
                    "error": 422,
                    "message": str(error)
                    }), 422

@app.errorhandler(404)
def notfond(error):
    return jsonify({
                    "success": False,
                    "error": 404,
                    "message": str(error)
                    }), 404

@app.errorhandler(405)
def notfond(error):
    return jsonify({
                    "success": False,
                    "error": 405,
                    "message": str(error)
                    }), 405


@app.errorhandler(500)
def internal(error):
    return jsonify({
                    "success": False,
                    "error": 500,
                    "message": str(error)
                    }), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, debug=True)
