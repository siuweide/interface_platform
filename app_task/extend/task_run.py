import json
import os
import sys
import time

import django
import xmlrunner

from ddt import ddt, file_data
import unittest
import requests

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__))) # 定位到你的django根目录
sys.path.append(os.path.abspath(os.path.join(BASE_DIR, os.pardir)))  # 把django目录放到环境变量里面
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "interface_platform.settings")  # django项目的配置，你的django的settings文件
django.setup()

from app_variable.models import Variable

EXTEND_DIR = os.path.dirname(os.path.abspath(__file__))
TASK_DATA = os.path.join(EXTEND_DIR, "task_data.json")
TASK_RESULTS = os.path.join(EXTEND_DIR, "task_results.xml")

@ddt
class RunCase(unittest.TestCase):

    @file_data(TASK_DATA)
    def test_file_data_json(self, id, url, method, header, req_body, req_type, assert_type, assert_body, assert_result, response_result, api_type_id):
        if method == "POST":
            if api_type_id == 3:
                res = requests.post(url, headers=json.loads(header), data=json.loads(req_body))
                cookies = requests.utils.dict_from_cookiejar(res.cookies)
                cookies = 'sessionid=' + cookies['sessionid']
                variable = Variable.objects.filter(key='Cookie')
                if variable:
                    for item in variable:
                        item.value = cookies
                        item.save()
                else:
                    Variable.objects.create(key="Cookie", value=cookies)
                if assert_type == 'include':
                    self.assertIn(assert_body, res.text)
                elif assert_type == 'equal':
                    self.assertEqual(assert_body, res.text)
            else:
                res = requests.post(url, headers=header, data=req_body).text
                if assert_type == 'include':
                    self.assertIn(assert_body, res)
                elif assert_type == 'equal':
                    self.assertEqual(assert_body, res)

        elif method == "GET":
            if api_type_id == 3:
                res = requests.get(url, headers=header, params=req_body)
                cookies = requests.utils.dict_from_cookiejar(res.cookies)
                cookies = 'sessionid=' + cookies['sessionid']
                variable = Variable.objects.create(key="Cookie", value=cookies)
                if variable:
                    for item in variable:
                        item.value = cookies
                        item.save()
                else:
                    Variable.objects.create(key="Cookie", value=cookies)
                if assert_type == 'include':
                    self.assertIn(assert_body, res.text)
                elif assert_type == 'equal':
                    self.assertEqual(assert_body, res.text)
            else:
                res = requests.post(url, headers=header, data=req_body).text
                if assert_type == 'include':
                    self.assertIn(assert_body, res)
                elif assert_type == 'equal':
                    self.assertEqual(assert_body, res)

if __name__ == '__main__':
    with open(TASK_RESULTS, 'wb') as output:
        unittest.main(
            testRunner=xmlrunner.XMLTestRunner(output=output),
            failfast=False, buffer=False, catchbreak=False)