import os
import sys
import time
import json
import django
import xmlrunner
import unittest
import requests
from ddt import ddt, file_data
from BeautifulReport import BeautifulReport

BASE_DIR_EXTEND = os.path.dirname(os.path.dirname(os.path.abspath(__file__))) # 定位到你的django根目录
sys.path.append(os.path.abspath(os.path.join(BASE_DIR_EXTEND, os.pardir)))  # 把django目录放到环境变量里面
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "interface_platform.settings")  # django项目的配置，你的django的settings文件
django.setup()

from util.Request import Request
from interface_platform.settings import BASE_DIR

EXTEND_DIR = os.path.dirname(os.path.abspath(__file__))
TASK_DATA = os.path.join(EXTEND_DIR, "task_data.json")
TASK_RESULTS = os.path.join(EXTEND_DIR, "task_results.xml")

@ddt
class RunCase(unittest.TestCase):

    @file_data(TASK_DATA)
    def test_file_data_json(self, id, url, method, header, req_body, req_type, assert_type, assert_body, assert_result, response_result, api_type_id):
        request = Request()
        if method == "POST":
            if api_type_id == 3:
                res = requests.post(url, headers=json.loads(header), data=json.loads(req_body))
                request.create_or_update_cookie(res)
                if assert_type == 'include':
                    self.assertIn(assert_body, res.text)
                elif assert_type == 'equal':
                    self.assertEqual(assert_body, res.text)
            else:
                if "${" in header and "}" in header:
                    # 获取真正的header
                    header = request.get_actual_header(header)

                if "${" in req_body and "}" in req_body:
                    # 获取真正的body
                    req_body = request.get_actual_body(req_body)

                res = requests.post(url, headers=json.loads(header), data=json.loads(req_body)).text
                request.judge_variable(res, aid=id)
                if assert_type == 'include':
                    self.assertIn(assert_body, res)
                elif assert_type == 'equal':
                    self.assertEqual(assert_body, res)
        elif method == "GET":
            if api_type_id == 3:
                res = requests.get(url, headers=header, params=req_body)
                request = Request()
                request.create_or_update_cookie(res)
                if assert_type == 'include':
                    self.assertIn(assert_body, res.text)
                elif assert_type == 'equal':
                    self.assertEqual(assert_body, res.text)
            else:
                # 获取真正的header
                if "${" in header and "}" in header:
                    header = request.get_actual_header(header)

                if "${" in req_body and "}" in req_body:
                    # 获取真正的body
                    req_body = request.get_actual_body(req_body)

                res = requests.get(url, headers=json.loads(header), params=json.loads(req_body)).text
                request.judge_variable(res, aid=id)
                if assert_type == 'include':
                    self.assertIn(assert_body, res)
                elif assert_type == 'equal':
                    self.assertEqual(assert_body, res)

if __name__ == '__main__':
    now = time.strftime('%Y-%m-%d_%H_%M_%S', time.localtime())
    filename = now + '.html'
    report_path = BASE_DIR + '/templates/report/'
    testsuite = unittest.makeSuite(RunCase)
    runner = BeautifulReport(testsuite)
    runner.report(description='接口测试报告', filename=filename, log_path=report_path)
    # with open(TASK_RESULTS, 'wb') as output:
    #     unittest.main(
    #         testRunner=xmlrunner.XMLTestRunner(output=output),
    #         failfast=False, buffer=False, catchbreak=False)
