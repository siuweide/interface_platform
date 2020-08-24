import os
import re
import sys
import json
import django
import requests
from jsonpath_rw import parse

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__))) # 定位到你的django根目录
sys.path.append(os.path.abspath(os.path.join(BASE_DIR, os.pardir)))  # 把django目录放到环境变量里面
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "interface_platform.settings")  # django项目的配置，你的django的settings文件
django.setup()

from app_variable.models import Variable

class Request():

    def create_or_update_cookie(self, res):
        # 创建或者更新cookie
        cookies = requests.utils.dict_from_cookiejar(res.cookies)
        cookies = 'sessionid=' + cookies['sessionid']
        variable = Variable.objects.filter(key='Cookie')
        if variable:
            for item in variable:
                item.value = cookies
                item.save()
        else:
            Variable.objects.create(key="Cookie", value=cookies)

    def get_actual_header(self, header):
        # 获取真正的整个header值
        key = re.findall("\${(.+?)}", header)
        variable = Variable.objects.filter(key=key[0])
        if variable:
            for v in variable:
                real_value = v.value
            data_list = re.findall("\"(.+?)\"", header)
            for data in data_list:
                if "${" in data and "}" in data:
                    replace_data = data
                    header = header.replace(replace_data, real_value)
                    return header

    def get_actual_body(self, req_body):
        # 获取真正的整个body值
        key = re.findall("\${(.+?)}", req_body)
        variable = Variable.objects.filter(key=key[0])
        if variable:
            for v in variable:
                real_value = v.value
            data_list = re.findall("\"(.+?)\"", req_body)
            for data in data_list:
                if "${" in data and "}" in data:
                    replace_data = data
                    req_body = req_body.replace(replace_data, real_value)
                    return req_body

    def judge_variable(self, res, aid):
        # 判断是否有接口用例是否有变量值，有的话就创建或修改
        variable = Variable.objects.filter(api_id=aid)
        if variable:
            variable_key = variable[0].key
            variable_extract_value = variable[0].extract_value
            real_value = ''
            response_data = json.loads(res)
            json_exe = parse(variable_extract_value)
            madle = json_exe.find(response_data)
            try:
                real_value = [math.value for math in madle][0]
            except IndexError:
                print('-----------------》没找到value')
            variable = Variable.objects.filter(key=variable_key)
            if variable:
                variable[0].extract_value = variable_extract_value
                variable[0].value = real_value
                variable[0].save()
            else:
                Variable.objects.create(key=variable_key, extract_value=variable_extract_value, value=real_value)