import json
import unittest


class TestFunctions(unittest.TestCase):

    def test_haversine_distance(self):
        # get testcases from testdata.py
        testcases =

        # check results for all testcases
        for case in testcases:
            input = case["input"]
            expect_res = case["expected"]

            # get the actual result
            res =

            # check if results are equal
            self.assertEqual(res, expect_res,
                             f"")

if __name__ == "__main__":
    unittest.main()
