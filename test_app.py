import os
import unittest
import json
from flask_sqlalchemy import SQLAlchemy

from app import create_app
from database.models import setup_db, Movie, Actor

ASSISTANT = "assistant_token"

DIRECTOR = "director_token"

PRODUCER = "producer_token"


class Capston_Test_Case(unittest.TestCase):

    def setUp(self):
        """Define test variables and initialize app."""
        self.app = create_app()
        self.client = self.app.test_client
        setup_db(self.app)

        with self.app.app_context():
            self.db = SQLAlchemy()
            self.db.init_app(self.app)
            self.db.create_all()

    def tearDown(self):
        """Executed after reach test"""
        pass

    def test_get_all_actors_without_auth(self):
        res = self.client().get('/actors')
        data = json.loads(res.data)

        self.assertFalse(data['success'])
        self.assertEqual(res.status_code, 401)


class Test_Assistant(unittest.TestCase):
    new_actor = {
        "name": "JH",
        "age": "20",
        "sex": "Female"
    }

    def setUp(self):
        """Define test variables and initialize app."""
        self.app = create_app()
        self.client = self.app.test_client
        self.headers = {'Content-Type': 'application/json',
                        'Authorization': f'Bearer {ASSISTANT}'}
        setup_db(self.app)

        with self.app.app_context():
            self.db = SQLAlchemy()
            self.db.init_app(self.app)
            self.db.create_all()

    def tearDown(self):
        """Executed after reach test"""
        pass

    def test_get_all_actors_wit_auth(self):
        res = self.client().get('/actors', headers=self.headers)
        data = json.loads(res.data)

        self.assertTrue(data['success'])
        self.assertEqual(res.status_code, 200)

    def test_get_all_movies_without_auth(self):
        res = self.client().get('/movies')
        data = json.loads(res.data)

        self.assertFalse(data['success'])
        self.assertEqual(res.status_code, 401)

    def test_get_all_movies_with_auth(self):
        res = self.client().get('/movies', headers=self.headers)
        data = json.loads(res.data)

        self.assertTrue(data['success'])
        self.assertEqual(res.status_code, 200)

    def test_create_actor_fail(self):
        res = self.client().post('/actors', headers=self.headers,
                                 json=self.new_actor)
        data = json.loads(res.data)

        self.assertFalse(data['success'])
        self.assertEqual(res.status_code, 401)


class Test_Director(unittest.TestCase):
    new_actor = {
        "name": "JH",
        "age": "20",
        "sex": "Female"
    }

    new_movie = {
        "title": "Sunshine",
        "release": "2020-02-02"
    }

    def setUp(self):
        """Define test variables and initialize app."""
        self.app = create_app()
        self.client = self.app.test_client
        self.headers = {'Content-Type': 'application/json',
                        'Authorization': f'Bearer {DIRECTOR}'}
        setup_db(self.app)

        with self.app.app_context():
            self.db = SQLAlchemy()
            self.db.init_app(self.app)
            self.db.drop_all()
            self.db.create_all()

    def tearDown(self):
        """Executed after reach test"""
        pass

    def test_create_actor_success(self):
        res = self.client().post('/actors', headers=self.headers,
                                 json=self.new_actor)
        data = json.loads(res.data)

        self.assertTrue(data['success'])
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['actor'].get("name"), self.new_actor.get("name"))
        self.assertEqual(data['actor'].get("sex"), self.new_actor.get("sex"))

    def test_create_movie_fail(self):
        res = self.client().post('/movies', headers=self.headers,
                                 json=self.new_movie)
        data = json.loads(res.data)

        self.assertFalse(data['success'])
        self.assertEqual(res.status_code, 401)

    def test_delete_actor_success(self):
        res = self.client().post('/actors', headers=self.headers,
                                 json=self.new_actor)
        data = json.loads(res.data)
        self.assertTrue(data['success'])
        id = data.get('actor').get('id')

        res = self.client().delete(f'/actors/{id}', headers=self.headers)
        data = json.loads(res.data)

        self.assertTrue(data['success'])
        self.assertEqual(res.status_code, 200)
        actors = data.get('actors')
        for actor in actors:
            self.assertNotEqual(actor.get("id"), id)

    def test_delete_movie_fail(self):
        res = self.client().delete('/movies/1', headers=self.headers)
        data = json.loads(res.data)

        self.assertFalse(data['success'])
        self.assertEqual(res.status_code, 401)


class Test_Producer(unittest.TestCase):
    new_actor = {
        "name": "JH",
        "age": "20",
        "sex": "Female"
    }

    updated_actor = {
        "name": "DH",
        "age": "20",
        "sex": "Female"
    }

    new_movie = {
        "title": "Sunshine",
        "release": "2020-02-02"
    }

    updated_movie = {
        "title": "Sunshine2",
        "release": "2020-02-02"
    }

    def setUp(self):
        """Define test variables and initialize app."""
        self.app = create_app()
        self.client = self.app.test_client
        self.headers = {'Content-Type': 'application/json',
                        'Authorization': f'Bearer {PRODUCER}'}
        setup_db(self.app)

        with self.app.app_context():
            self.db = SQLAlchemy()
            self.db.init_app(self.app)
            self.db.create_all()

    def tearDown(self):
        """Executed after reach test"""
        pass

    def test_delete_movie_success(self):
        res = self.client().post('/movies', headers=self.headers,
                                 json=self.new_movie)
        data = json.loads(res.data)
        self.assertTrue(data['success'])
        id = data.get('movie').get('id')

        res = self.client().delete(f'/movies/{id}', headers=self.headers)
        data = json.loads(res.data)

        self.assertTrue(data['success'])
        self.assertEqual(res.status_code, 200)

        movies = data.get('movies')
        for movie in movies:
            self.assertNotEqual(movie.get("id"), id)

    def test_update_actor_sucess(self):
        res = self.client().post('/actors', headers=self.headers,
                                 json=self.new_actor)
        data = json.loads(res.data)
        self.assertTrue(data['success'])
        id = data.get('actor').get('id')

        res = self.client().patch(f'/actors/{id}', headers=self.headers,
                                  json=self.updated_actor)
        data = json.loads(res.data)

        self.assertTrue(data['success'])
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data.get("actor").get('id'), id)
        self.assertEqual(data.get("actor").get('name'),
                         self.updated_actor.get("name"))

    def test_update_movie_sucess(self):
        id = 1
        res = self.client().post('/movies', headers=self.headers,
                                 json=self.new_movie)
        data = json.loads(res.data)
        self.assertTrue(data['success'])
        id = data.get('movie').get('id')

        res = self.client().patch(f'/movies/{id}', headers=self.headers,
                                  json=self.updated_movie)
        data = json.loads(res.data)

        self.assertTrue(data['success'])
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data.get("movie").get('id'), id)
        self.assertEqual(data.get("movie").get('title'),
                         self.updated_movie.get("title"))


if __name__ == "__main__":
    unittest.main()
