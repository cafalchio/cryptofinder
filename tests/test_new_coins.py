import unittest
from backend.data.models import AllCoins
from tests.utils import BaseTestCase, logger
from datetime import datetime
from app.app import db
from bs4 import BeautifulSoup
import json


class TestRoutes(BaseTestCase):

    def test_new_coins_today(self):
        coin = {
            "id": "dummy",
            "symbol": "dummySymbol",
            "name": "dummy",
        }
        expected = "dummySymbol"
        dummy_coin = AllCoins(
            id=coin["id"],
            symbol=coin["symbol"],
            name=coin["name"]
        )
        with self.app.app_context():
            db.session.add(dummy_coin)
            db.session.commit()
            response = self.client.get('/')
        soup = BeautifulSoup(response.data, 'html.parser')
        actual = [td.text for td in soup.findAll("td")]
        self.assertIn(expected, actual)

    def test_all_coins(self):
        response = self.client.get('/all_coins')
        self.assertEqual(response.status_code, 200)

    def test_shitcoins(self):
        response = self.client.get('/shitcoins')
        self.assertEqual(response.status_code, 200)

    def test_log(self):
        response = self.client.get('/log')
        self.assertEqual(response.status_code, 200)


if __name__ == '__main__':
    unittest.main()
