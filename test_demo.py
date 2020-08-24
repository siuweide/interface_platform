import os
import time
import unittest
import requests
from ddt import ddt, file_data
from BeautifulReport import BeautifulReport

@ddt
class RunCase(unittest.TestCase):

    @file_data('./test_data.json')
    def test_file_data_json(self, method, url, data):
        if method == "post":
            res = requests.post(url, data)
            print(res.text)

if __name__ == '__main__':
    now = time.strftime('%Y-%m-%d_%H_%M_%S', time.localtime())
    filename = now + '.html'
    report_path = os.path.abspath(os.path.dirname(__file__)) + '/report/'
    testsuite = unittest.makeSuite(RunCase)
    runner = BeautifulReport(testsuite)
    runner.report(description='接口测试报告', filename=filename, log_path=report_path)