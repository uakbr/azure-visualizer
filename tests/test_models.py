import unittest
from app import db, create_app
from app.models import User, Permission
from datetime import datetime, timedelta

class UserModelCase(unittest.TestCase):
    def setUp(self):
        self.app = create_app('testing')
        self.app_context = self.app.app_context()
        self.app_context.push()
        db.create_all()

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    def test_password_hashing(self):
        u = User(username='john', email='john@example.com', password='cat')
        self.assertFalse(u.password == 'cat')

    def test_avatar(self):
        u = User(username='john', email='john@example.com', password='cat')
        self.assertEqual(u.image_file, 'default.jpg')

    def test_repr(self):
        u = User(username='john', email='john@example.com', password='cat')
        self.assertEqual(u.__repr__(), "User('john', 'john@example.com', 'default.jpg')")

class PermissionModelCase(unittest.TestCase):
    def setUp(self):
        self.app = create_app('testing')
        self.app_context = self.app.app_context()
        self.app_context.push()
        db.create_all()

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    def test_permission_creation(self):
        u = User(username='susan', email='susan@example.com', password='dog')
        db.session.add(u)
        db.session.commit()
        p = Permission(service_name='Azure Storage', access_level='Read', user_id=u.id)
        db.session.add(p)
        db.session.commit()
        self.assertTrue(p in u.permissions)

    def test_permission_repr(self):
        p = Permission(service_name='Azure Storage', access_level='Read', date_assigned=datetime.utcnow())
        self.assertTrue("Permission('Azure Storage', 'Read'" in p.__repr__())

if __name__ == '__main__':
    unittest.main()
