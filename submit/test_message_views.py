"""Message View tests."""

# run these tests like:
#
#    FLASK_ENV=production python -m unittest test_message_views.py


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

# Don't have WTForms use CSRF at all, since it's a pain to test

app.config['WTF_CSRF_ENABLED'] = False


class MessageViewTestCase(TestCase):
    """Test views for messages."""

    def setUp(self):
        """Create test client, add sample data."""

        User.query.delete()
        Message.query.delete()

        self.client = app.test_client()

        self.testuser = User.signup(username="testuser",
                                    email="test@test.com",
                                    password="testuser",
                                    image_url=None)

        db.session.commit()

    def test_add_message(self):
        """Can use add a message?"""

        # Since we need to change the session to mimic logging in,
        # we need to use the changing-session trick:

        with self.client as c:
            with c.session_transaction() as sess:
                sess[CURR_USER_KEY] = self.testuser.id

            # Now, that session setting is saved, so we can have
            # the rest of ours test

            resp = c.post("/messages/new", data={"text": "Hello"})

            # Make sure it redirects
            self.assertEqual(resp.status_code, 302)

            msg = Message.query.one()
            self.assertEqual(msg.text, "Hello")

            #######################################

def test_msg_invalid(self):
    with self.client as cli:
        with cli.session_transaction() as session:
            session[CURR_USER_KEY] = self.testuser.id
        response = cli.get('/messages/9876543')
        self.assertEqual(response.status_code, 404)

def test_invalid(self):
    with self.client as cli:
        with cli.session_transaction() as session:
            session[CURR_USER_KEY] = 10000000 
        resp = cli.post("/messages/new", data={"text": "yo"}, follow_redirects=True)
        self.assertEqual(resp.status_code, 200)
        self.assertIn("Access unauthorized", str(resp.data))

def test_unauthorized(self):
    with self.client as cli:
        resp = cli.post("/messages/new", data={"text": "hi"}, follow_redirects=True)
        self.assertEqual(resp.status_code, 200)
        self.assertIn("Access unauthorized", str(resp.data))        

def test_msg_delete(self):
    message = Message(
        id=9999,
        text="test",
        user_id=self.testuser_id
    )
    db.session.add(message)
    db.session.commit()
    with self.client as cli:
        with cli.session_transaction() as session:
            session[CURR_USER_KEY] = self.testuser.id
        response = c.post("/messages/9999/delete", follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        message = Message.query.get(9999)
        self.assertIsNone(message)

def test_delete(self):
    user = User.signup(username="user",
                    email="user@example.com",
                    password="abc123",
                    image_url=None)
    user.id = 99999
    message = Message(
        id=99999,
        text="test",
        user_id=self.testuser_id
    )
    db.session.add_all([user, message])
    db.session.commit()
    with self.client as cli:
        with cli.session_transaction() as session:
            session[CURR_USER_KEY] = 99999
        response = cli.post("/messages/99999/delete", follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assertIn("Access unauthorized", str(response.data))
        message = Message.query.get(99999)
        self.assertIsNotNone(message)

def test_cant_delete(self):
    message = Message(
        id=99999,
        text="test",
        user_id=self.testuser_id
    )
    db.session.add(message)
    db.session.commit()
    with self.client as cli:
        response = c.post("/messages/99999/delete", follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assertIn("unauthorized", str(response.data))
        message = Message.query.get(99999)
        self.assertIsNotNone(message)

def test_show(self):
    message = Message(
        id=999999,
        text="message",
        user_id=self.testuser_id
    )
    db.session.add(message)
    db.session.commit()
    with self.client as cli:
        with cli.session_transaction() as session:
            session[CURR_USER_KEY] = self.testuser.id
        message = Message.query.get(99999)
        resp = cli.get(f'/messages/{message.id}')
        self.assertEqual(resp.status_code, 200)
        self.assertIn(message.text, str(resp.data))
