import json
import unittest
from backend.app.utility_scripts import haversine_distance

class TestFunctions(unittest.TestCase):

    def test_haversine_distance(self):
        # get testcases from testdata.py
        testcases = []

        # Check results for all testcases
        for case in testcases:
            input_values = case["input"]
            expected_result = case["expected"]

            # Get the actual result
            actual_result = haversine_distance(*input_values)

            # Check if results are equal
            self.assertEqual(actual_result,
                            expected_result,
                             f"Failed for input {input_values}. Expected distance: {expected_result} km, but got: {actual_result} km.")

if __name__ == "__main__":
    unittest.main()
