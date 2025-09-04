import datetime
import unittest
from backend.data.models import AllCoins
from tests.utils import BaseTestCase
from bs4 import BeautifulSoup

# TODO: Add more tests


class TestRoutes(BaseTestCase):
    def test_new_coins_today(self):
        endpoint = "/"
        expected = "dummySymbol"

        self.add_coins_to_db([AllCoins(id="id", symbol="dummySymbol", name="dummy")])

        response = self.get_response(endpoint)
        soup = BeautifulSoup(response.data, "html.parser")
        actual = [td.text for td in soup.findAll("td")]
        self.assertIn(expected, actual)

    def test_new_coins_with_expired(self):
        endpoint = "/"
        expected = "dummySymbol"
        not_expected = "expired"
        yesterday = datetime.datetime.utcnow() - datetime.timedelta(days=2)
        coins = [
            AllCoins(id="id", symbol="dummySymbol", name="dummy"),
            AllCoins(id="id1", symbol="expiredSymbol", name="expired", added=yesterday),
        ]
        self.add_coins_to_db(coins)
        response = self.get_response(endpoint)
        soup = BeautifulSoup(response.data, "html.parser")
        actual = [td.text for td in soup.findAll("td")]
        self.assertIn(expected, actual)
        self.assertNotIn(not_expected, actual)

    def test_all_coins(self):
        endpoint = "/all_coins"
        expected = "expired"
        yesterday = datetime.datetime.utcnow() - datetime.timedelta(days=2)
        coins = [
            AllCoins(id="id", symbol="dummySymbol", name="dummy"),
            AllCoins(id="id1", symbol="expiredSymbol", name="expired", added=yesterday),
        ]
        self.add_coins_to_db(coins)
        response = self.get_response(endpoint)
        soup = BeautifulSoup(response.data, "html.parser")
        actual = [td.text for td in soup.findAll("td")]
        self.assertIn(expected, actual)

    def test_log(self):
        response = self.client.get("/log")
        self.assertEqual(response.status_code, 200)


if __name__ == "__main__":
    unittest.main()
