import os
import unittest
import json
from flask_sqlalchemy import SQLAlchemy

from app import create_app
from database.models import setup_db, Movie, Actor

ASSISTANT = "eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6Ik1VTXdPVGcyUkRjNE16WXhRalU1TVVNeE9UZ3lPRFpDTnpCQlFUVTFRMEZET0VZelFqRXlNQSJ9.eyJpc3MiOiJodHRwczovL2ppbmhlZS5hdXRoMC5jb20vIiwic3ViIjoiYXV0aDB8NWU1ZjBiYWE4OGVjMTcwZDZiOGZiODc1IiwiYXVkIjoiYWdlbmN5IiwiaWF0IjoxNTgzMzE5MTIxLCJleHAiOjE1ODMzMjYzMjEsImF6cCI6InpiazVyS08zYnpUcXNsRG5Zb0Z2aDNTZ2N2d0RoaVFuIiwic2NvcGUiOiIiLCJwZXJtaXNzaW9ucyI6WyJnZXQ6YWN0b3JzIiwiZ2V0Om1vdmllcyJdfQ.GXixzfGv1IamBBlExKvO6c6KsIpD7M_z6yfC-B3Qd5T5GdZlybOHAfJU10GFn8nFhopDfEesTPOriofNILiZLeTD-n0EPQ2EezSxIiZPSAWhY65gtft9as1mm8EhPh4J4poM07ygxU0rY17n6Rct4EdoNsQMOh20my6IRgxBh6ZH3R_TMplipM9BnFDYEzoQaGdVozMfET0TXKV46jBpP9a8VMjQZcczNjQ-drJW9nOTq0tzgiXJC1KRCRxWVJGvijv3TD36TUqMrrjaW8dqABPx6Y8hbByRjf7So1iXN1Y819yIQJ3IPvhqCF_lTWshafMdUmLAoNHDMzjkqUsf0Q"

DIRECTOR = "eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6Ik1VTXdPVGcyUkRjNE16WXhRalU1TVVNeE9UZ3lPRFpDTnpCQlFUVTFRMEZET0VZelFqRXlNQSJ9.eyJpc3MiOiJodHRwczovL2ppbmhlZS5hdXRoMC5jb20vIiwic3ViIjoiYXV0aDB8NWU1ZjBiZDhjZTljODIwZDVlMWQwN2YyIiwiYXVkIjoiYWdlbmN5IiwiaWF0IjoxNTgzMzE5MjEzLCJleHAiOjE1ODMzMjY0MTMsImF6cCI6InpiazVyS08zYnpUcXNsRG5Zb0Z2aDNTZ2N2d0RoaVFuIiwic2NvcGUiOiIiLCJwZXJtaXNzaW9ucyI6WyJkZWxldGU6YWN0b3JzIiwiZ2V0OmFjdG9ycyIsImdldDptb3ZpZXMiLCJwYXRjaDphY3RvcnMiLCJwYXRjaDptb3ZpZXMiLCJwb3N0OmFjdG9ycyJdfQ.QM4pMH8nSU3HY7ALXdcxGxv1yx_rbvTtSgOdSJ03u55nPWrofMVTbDVV4kNu2IxVCl9sdv9RFxszvOhbFkJfNR8ma9g35lPwkk217lZvPyByRTog3bs29jpiZuSMtVx10bnEOUoTCUkyQOgFCkp2tV6d6ptokAM0WR4gOuiH9ii_ZLTXAdR4Yfh_2vFZitHpnWp5Nsmcrfi9KPJBVnnJqEkgQupcC5EHgYEO86Drukbsm_R_0k52ZC6nU3Ga0zy_4fKEQxPoKPuzYk9eMBo0_mP4S0a5k7i27DJyAWMtnBgedl_uNRpeSFfUwEg6rFxR_AahFF3XFjKPi2ohWsJl8A"

PRODUCER = "eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6Ik1VTXdPVGcyUkRjNE16WXhRalU1TVVNeE9UZ3lPRFpDTnpCQlFUVTFRMEZET0VZelFqRXlNQSJ9.eyJpc3MiOiJodHRwczovL2ppbmhlZS5hdXRoMC5jb20vIiwic3ViIjoiYXV0aDB8NWU1ZjBiZmFjZTljODIwZDVlMWQwODU1IiwiYXVkIjoiYWdlbmN5IiwiaWF0IjoxNTgzMzE5Mjk5LCJleHAiOjE1ODMzMjY0OTksImF6cCI6InpiazVyS08zYnpUcXNsRG5Zb0Z2aDNTZ2N2d0RoaVFuIiwic2NvcGUiOiIiLCJwZXJtaXNzaW9ucyI6WyJkZWxldGU6YWN0b3JzIiwiZGVsZXRlOm1vdmllcyIsImdldDphY3RvcnMiLCJnZXQ6bW92aWVzIiwicGF0Y2g6YWN0b3JzIiwicGF0Y2g6bW92aWVzIiwicG9zdDphY3RvcnMiLCJwb3N0Om1vdmllcyJdfQ.XaXXjP-g0JIo4mHhtP559Oo4R9rdijOcjz1BHvogHsDJYxr961yB0n-Q9ZUszAgAgWzhH5gamaAlfLGtr9VAukqNVHr7LIQZGGdwAj0ROB0dSK_ZTs6D84OX5BNiG91hX38O9PkxrjbBJWbOHvqwaZG95qqR0ZyP8c1ZXbrmaRvakTbO2hDWT17pfiKN35VEHRWbVNtHKDr40UpuZ6ndwMs5Esk2rPaz597N0IzYe6oFn9TFiWod3OB2PCW-U1FImqqfU4k6Sj79id3do4KPi-gcIsjzoa9HOqJ2rj1xMKKdtgePU8finBjrWLszDw306kriHF_j7w23UVUT58bn5A"

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
        self.headers = {'Content-Type': 'application/json', 'Authorization': f'Bearer {ASSISTANT}'}
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
        res = self.client().post('/actors', headers=self.headers, json=self.new_actor)
        data = json.loads(res.data)

        self.assertFalse(data['success'])
        self.assertEqual(res.status_code, 401)
# self.assertEqual(data['actor'].get("name"), self.new_actor.get("name"))


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
        self.headers = {'Content-Type': 'application/json', 'Authorization': f'Bearer {DIRECTOR}'}
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
        res = self.client().post('/actors', headers=self.headers, json=self.new_actor)
        data = json.loads(res.data)

        self.assertTrue(data['success'])
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['actor'].get("name"), self.new_actor.get("name"))
        self.assertEqual(data['actor'].get("sex"), self.new_actor.get("sex"))

    def test_create_movie_fail(self):
        res = self.client().post('/movies', headers=self.headers, json=self.new_movie)
        data = json.loads(res.data)

        self.assertFalse(data['success'])
        self.assertEqual(res.status_code, 401)

    def test_delete_actor_success(self):
        res = self.client().post('/actors', headers=self.headers, json=self.new_actor)
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
        self.headers = {'Content-Type': 'application/json', 'Authorization': f'Bearer {PRODUCER}'}
        setup_db(self.app)

        with self.app.app_context():
            self.db = SQLAlchemy()
            self.db.init_app(self.app)
            self.db.create_all()

    def tearDown(self):
        """Executed after reach test"""
        pass

    def test_delete_movie_success(self):
        res = self.client().post('/movies', headers=self.headers, json=self.new_movie)
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
        res = self.client().post('/actors', headers=self.headers, json=self.new_actor)
        data = json.loads(res.data)
        self.assertTrue(data['success'])
        id = data.get('actor').get('id')

        res = self.client().patch(f'/actors/{id}', headers=self.headers, json=self.updated_actor)
        data = json.loads(res.data)

        self.assertTrue(data['success'])
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data.get("actor").get('id'), id)
        self.assertEqual(data.get("actor").get('name'), self.updated_actor.get("name"))

    def test_update_movie_sucess(self):
        id = 1
        res = self.client().post('/movies', headers=self.headers, json=self.new_movie)
        data = json.loads(res.data)
        self.assertTrue(data['success'])
        id = data.get('movie').get('id')

        res = self.client().patch(f'/movies/{id}', headers=self.headers, json=self.updated_movie)
        data = json.loads(res.data)

        self.assertTrue(data['success'])
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data.get("movie").get('id'), id)
        self.assertEqual(data.get("movie").get('title'), self.updated_movie.get("title"))

if __name__ == "__main__":
    unittest.main()
