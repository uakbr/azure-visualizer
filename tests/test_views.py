import unittest
from flask import url_for
from flask_testing import TestCase

from app import app, db
from app.models import User

class TestViews(TestCase):
    # Set up the application for testing
    def create_app(self):
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
        app.config['TESTING'] = True
        app.config['WTF_CSRF_ENABLED'] = False
        return app

    # Set up the database for each test
    def setUp(self):
        db.create_all()
        user1 = User(email="testuser@example.com", password="testpassword")
        db.session.add(user1)
        db.session.commit()

    # Tear down the database after each test
    def tearDown(self):
        db.session.remove()
        db.drop_all()

    # Test the home page view
    def test_home_page(self):
        response = self.client.get(url_for('home'))
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"Welcome to Azure Permissions Visualizer", response.data)

    # Test the login page loads correctly
    def test_login_page_loads(self):
        response = self.client.get(url_for('login'))
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"Login", response.data)

    # Test the login functionality with correct credentials
    def test_login_correct_credentials(self):
        response = self.client.post(url_for('login'), data=dict(email="testuser@example.com", password="testpassword"), follow_redirects=True)
        self.assertIn(b"Home", response.data)

    # Test the login functionality with incorrect credentials
    def test_login_incorrect_credentials(self):
        response = self.client.post(url_for('login'), data=dict(email="wronguser@example.com", password="wrongpassword"), follow_redirects=True)
        self.assertIn(b"Login Unsuccessful", response.data)

    # Test the logout functionality
    def test_logout(self):
        self.client.post(url_for('login'), data=dict(email="testuser@example.com", password="testpassword"), follow_redirects=True)
        response = self.client.get(url_for('logout'), follow_redirects=True)
        self.assertIn(b"Login", response.data)

if __name__ == '__main__':
    unittest.main()
