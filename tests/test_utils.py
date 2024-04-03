import unittest
import pandas as pd
from unittest.mock import patch
from app.utils import Table

class TestTable(unittest.TestCase):
    @patch('app.utils.Table.get_today', lambda x: pd.read_csv("./mock_today.csv"))
    @patch('app.utils.Table.get_yesterday', lambda x: pd.read_csv("./mock_yesterday.csv"))
    def test_get_differences(self):
        table = Table()
        differences = table.get_differences()
        expected_differences = ["ltc"]
        print(f"diff {differences} - {expected_differences}: {differences == expected_differences}")
        self.assertTrue(differences == expected_differences)

if __name__ == '__main__':
    unittest.main()
