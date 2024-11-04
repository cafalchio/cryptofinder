import unittest
from backend.data.models import AllCoins
from tests.utils import BaseTestCase
from bs4 import BeautifulSoup


class TestRoutes(BaseTestCase):

    def test_new_coins_today(self):

        endpoint = "/"
        expected = "dummySymbol"

        self.add_coins_to_db(
            [AllCoins(id="id", symbol="dummySymbol", name="dummy")]
        )

        response = self.get_response(endpoint)
        soup = BeautifulSoup(response.data, "html.parser")
        actual = [td.text for td in soup.findAll("td")]
        self.assertIn(expected, actual)

    def test_all_coins(self):
        response = self.client.get("/all_coins")
        self.assertEqual(response.status_code, 200)

    def test_shitcoins(self):
        response = self.client.get("/shitcoins")
        self.assertEqual(response.status_code, 200)

    def test_log(self):
        response = self.client.get("/log")
        self.assertEqual(response.status_code, 200)


if __name__ == "__main__":
    unittest.main()
