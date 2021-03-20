import os
from unittest import *
from sqlalchemy import *
from models import *

os.environ['DATABASE_URL'] = "postgresql:///warbler-test"

from app import *

db.create_all()

class TestUser(TestCase):
    def setUp(self):
        db.drop_all()
        db.create_all()
        self.uid = 99999
        user = User.signup("test", "user@example.com", "123abc", None)
        user.id = self.uid
        db.session.commit()
        self.user = User.query.get(self.uid)
        self.client = app.test_client()

    def test_likes(self):
        message1 = Message(
            text="test1",
            user_id=self.uid
        )
        message2 = Message(
            text="test2",
            user_id=self.uid 
        )
        user = User.signup("test2", "user@example.com", "123abc", None)
        uid = 99998
        user.id = uid
        db.session.add_all([message1, message2, user])
        db.session.commit()
        user.likes.append(message1)
        db.session.commit()
        like = Likes.query.filter(Likes.user_id == uid).all()
        self.assertEqual(len(like), 1)
        self.assertEqual(like[0].message_id, message1.id)

    def test_message(self):
        message = Message(
            text="test",
            user_id=self.uid
        )
        db.session.add(message)
        db.session.commit()
        self.assertEqual(len(self.u.messages), 1)
        self.assertEqual(self.u.messages[0].text, "test")

    def tearDown(self):
        result = super().tearDown()
        db.session.rollback()
        return result        