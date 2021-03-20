
import os
from unittest import TestCase

from models import *
from bs4 import *
os.environ['DATABASE_URL'] = "postgresql:///warbler-test"
from app import *

db.create_all()

app.config['WTF_CSRF_ENABLED'] = False

class MessageViewTestCase(TestCase):
    def setUp(self):
        db.drop_all()
        db.create_all()
        self.client = app.test_client()
        self.john = User.signup(username="john",email="john@example.com",password="abc123",image_url=None)
        self.john.id = 9999
        self.chuck = User.signup("chuck", "chuck@example.com", "abc123", None)
        self.chuck.id = 9998
        self.amy = User.signup("amy", "amy@example.com", "abc123", None)
        self.amy.id = 9997
        self.todd = User.signup("todd", "todd@example.com", "abc123", None)
        self.arnold = User.signup("arnold", "arnold@example.com", "abc123", None)
        db.session.commit()

    def tearDown(self):
        respond = super().tearDown()
        db.session.rollback()
        return respond

    def test_show(self):
        with self.client as cli:
            response = cli.get(f"/users/{self.john_id}")
            self.assertEqual(response.status_code, 200)
            self.assertIn("@john", str(response.data))          

    def test_follows(self):
        self.setup_followers()
        with self.client as cli:
            response = cli.get(f"/users/{self.john_id}")
            self.assertEqual(response.status_code, 200)
            self.assertIn("@john", str(response.data))
            b_soup = BeautifulSoup(str(response.data), 'html.parser')
            found = b_soup.find_all("li", {"class": "stat"})
            self.assertEqual(len(found), 4)
            self.assertIn("0", found[0].text)
            self.assertIn("2", found[1].text)
            self.assertIn("1", found[2].text)
            self.assertIn("0", found[3].text)

    def test_followers(self):
        self.setup_followers()
        with self.client as cli:
            with cli.session_transaction() as sess:
                sess[CURR_USER_KEY] = self.john_id
            resp = cli.get(f"/users/{self.john_id}/followers")
            self.assertIn("@amy", str(resp.data))
            self.assertNotIn("@todd", str(resp.data))
            self.assertNotIn("@arnold", str(resp.data))
            self.assertNotIn("@chuck", str(resp.data))                   

    def test_following(self):
        self.setup_followers()
        with self.client as cli:
            with cli.session_transaction() as sess:
                sess[CURR_USER_KEY] = self.john_id
            resp = cli.get(f"/users/{self.john_id}/following")
            self.assertEqual(resp.status_code, 200)
            self.assertIn("@amy", str(resp.data))
            self.assertIn("@todd", str(resp.data))
            self.assertNotIn("@arnold", str(resp.data))
            self.assertNotIn("@chuck", str(resp.data))

    def test_access(self):
        self.setup_followers()
        with self.client as cli:
            resp = cli.get(f"/users/{self.john_id}/following", follow_redirects=True)
            self.assertEqual(resp.status_code, 200)
            self.assertNotIn("@amy", str(resp.data))
            self.assertIn("Access unauthorized", str(resp.data))     



