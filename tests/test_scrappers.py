import unittest
from backend.scrappers.run_scrappers import update_all_coins
from tests.utils import BaseTestCase


class TestScrappers(BaseTestCase):
    def test_update_all_coins_no_coins(self):
        expected = None
        actual = update_all_coins([])
        self.assertEqual(expected, actual)

    # @patch("app.app.create_app")
    # def test_update_all_coins(self, mock_create_app):
    #     mock_create_app.return_value = self.app

    #     # Define test data
    #     coins = {
    #         "id2": AllCoins(id="id2", symbol="symbol0", name="dummy"),
    #         "id3": AllCoins(id="id3", symbol="symbol1", name="dummy1"),
    #     }
    #     update_all_coins(coins)
    #     with self.app.app_context():
    #         actual = db.session.execute(db.select(AllCoins)).scalars().all()

    #     expected = list(coins.values())
    #     self.assertListEqual(expected, actual)


if __name__ == "__main__":
    unittest.main()
