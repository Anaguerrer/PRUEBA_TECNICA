import datetime
import unittest
from utils import functions, dataforTesting


class TestFunctions(unittest.TestCase):
    def test_get_dates(self):
        self.assertEqual(functions.get_dates(), ['1650499200', '1650412800', '1650326400', '1650240000', '1650153600'])

    def test_get_arr_temps_5days(self):
        self.assertEqual(functions.get_arr_temps_5days(dataforTesting.data_example), dataforTesting.temp_response)

    def test_get_arr_hum_2days(self):
        self.assertEqual(functions.get_arr_hum_2days(dataforTesting.data_example), dataforTesting.humidity_response)


if __name__ == '__main__':
    unittest.main()