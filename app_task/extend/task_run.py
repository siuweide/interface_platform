import os
import time
import xmlrunner

from ddt import ddt, file_data
import unittest
import requests

EXTEND_DIR = os.path.dirname(os.path.abspath(__file__))
TASK_DATA = os.path.join(EXTEND_DIR, "task_data.json")
TASK_RESULTS = os.path.join(EXTEND_DIR, "task_results.xml")

@ddt
class RunCase(unittest.TestCase):

    @file_data(TASK_DATA)
    def test_file_data_json(self, url, method, header, req_body, req_type, assert_type, assert_body, assert_result, response_result):
        if method == "POST":
            res = requests.post(url, headers=header, data=req_body).text
            if assert_type == 'include':
                self.assertIn(assert_body, res)
            elif assert_type == 'equal':
                self.assertEqual(assert_body, res)
        elif method == "GET":
            res = requests.get(url, headers=header, params=req_body).text
            if assert_type == 'include':
                self.assertIn(assert_body, res)
            elif assert_type == 'equal':
                self.assertEqual(assert_body, res)

if __name__ == '__main__':
    with open(TASK_RESULTS, 'wb') as output:
        unittest.main(
            testRunner=xmlrunner.XMLTestRunner(output=output),
            failfast=False, buffer=False, catchbreak=False)