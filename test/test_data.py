import sys, os
import unittest

import pandas as pd
from backend.data import convert_df_dict
sys.path.insert(0, os.path.dirname(__file__))


class TestData(unittest.TestCase):

    def test_convert_df_dict_empty(self):
        df = pd.DataFrame([])
        self.assertEqual(convert_df_dict(df), {}, "")

