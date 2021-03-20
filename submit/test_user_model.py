"""User model tests."""

# run these tests like:
#
#    python -m unittest test_user_model.py


import os
from unittest import *

from models import *

# BEFORE we import our app, let's set an environmental variable
# to use a different database for tests (we need to do this
# before we import our app, since that will have already
# connected to the database

os.environ['DATABASE_URL'] = "postgresql:///warbler-test"


# Now we can import app

from app import *

# Create our tables (we do this here, so we only create the tables
# once for all tests --- in each test, we'll delete the data
# and create fresh new clean test data

db.create_all()


class UserModelTestCase(TestCase):
    def setUp(self):
        User.query.delete()
        Message.query.delete()
        Follows.query.delete()
        self.client = app.test_client()
        chuck = User.signup("chuck", "chuck@example.com", "password", None)
        chuck_id = 99999
        chuck.id = chuck_id
        amy = User.signup("amy", "amy@example.com", "password", None)
        amy_id = 99998
        amy.id = amy_id
        db.session.commit()
        chuck = User.query.get(chuck_id)
        amy = User.query.get(amy_id)
        self.chuck = chuck
        self.chuck_id = chuck_id
        self.amy = amy
        self.amy_id = amy_id
        self.client = app.test_client()

    def test_user(self):
        user = User(
            email="user@example.com",
            username="user",
            password="abc123"
        )
        db.session.add(user)
        db.session.commit()
        self.assertEqual(len(user.messages), 0)
        self.assertEqual(len(user.followers), 0)

    def test_following(self):
        self.chuck.following.append(self.amy)
        db.session.commit()
        self.assertTrue(self.chuck.is_following(self.amy))
        self.assertFalse(self.amy.is_following(self.chuck))

    def test_follows(self):
        self.chuck.following.append(self.amy)
        db.session.commit()
        self.assertEqual(len(self.amy.following), 0)
        self.assertEqual(len(self.amy.followers), 1)
        self.assertEqual(len(self.chuck.followers), 0)
        self.assertEqual(len(self.chuck.following), 1)
        self.assertEqual(self.amy.followers[0].id, self.chuck.id)
        self.assertEqual(self.chuck.following[0].id, self.amy.id)

    def test_valid(self):
        user_test = User.signup("user", "user@example.com", "abc123", None)
        user_id = 99999
        user_test.id = user_id
        db.session.commit()
        user_test = User.query.get(user_id)
        self.assertIsNotNone(user_test)
        self.assertEqual(user_test.username, "user")
        self.assertEqual(user_test.email, "user@example.com")
        self.assertNotEqual(user_test.password, "abc123")

    def test_followed(self):
        self.chuck.following.append(self.amy)
        db.session.commit()
        self.assertTrue(self.amy.is_followed_by(self.chuck))
        self.assertFalse(self.chuck.is_followed_by(self.amy))

    def test_password(self):
        with self.assertRaises(ValueError) as context:
            User.signup("test", "user@example.com", "", None)
        
        with self.assertRaises(ValueError) as context:
            User.signup("test", "user@example.com", None, None)

    def test_username(self):
        invalid = User.signup(None, "user@example.com", "abc123", None)
        user_id = 99999
        invalid.id = user_id
        with self.assertRaises(exc.IntegrityError) as context:
            db.session.commit()

    def test_email(self):
        invalid = User.signup("test", None, "abc123", None)
        user_id = 99999
        invalid.id = user_id
        with self.assertRaises(exc.IntegrityError) as context:
            db.session.commit()
    
    def test_authentication(self):
        user = User.authenticate(self.chuck.username, "abc123")
        self.assertIsNotNone(user)
        self.assertEqual(user.id, self.chuck_id)

    def test_password(self):
        self.assertFalse(User.authenticate(self.chuck.username, "abc123"))

    def test_invalid(self):
        self.assertFalse(User.authenticate("test", "abc123"))

    def tearDown(self):
        result = super().tearDown()
        db.session.rollback()
        return result


        




        

