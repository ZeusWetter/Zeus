import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
import json
import unittest
from backend.app.utility_scripts import haversine_distance
import testdata

class TestFunctions(unittest.TestCase):

    def test_haversine_distance(self):
        # get testcases from testdata.py
        testcases = testdata.testdata_haversine

        # Check results for all testcases
        for case in testcases:
            input_values = case["input"]
            expected_result = case["expected"]

            # Get the actual result
            actual_result = haversine_distance(*input_values)

            # Check if results are equal
            self.assertAlmostEqual(actual_result,
                            expected_result,
                             msg=f"Failed for input {input_values}. Expected distance: {expected_result} km, but got: {actual_result} km.",
                             delta=1)

if __name__ == "__main__":
    unittest.main()
