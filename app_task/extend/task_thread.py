import os
import json
import threading
from time import sleep
from xml.etree import ElementTree

from app_api.models import ApiCase
from app_task.models import Task, TestReport
from app_task.setting import TASK_DATA, TASK_RUN, TASK_RESULT


class TaskThread():

    def __init__(self, task_id):
        self.task_id = task_id

    def run_task(self):
        # 1、通过任务id获取case用例数
        task = Task.objects.get(id=self.task_id)
        # 将任务改为执行中
        task.status = 1
        task.save()

        str_cases = task.cases
        case_list = str_cases[1:-1].split(',')
        case_list = [int(x) for x in case_list]
        api_info_data = {}
        for case_id in case_list:
            api_case = ApiCase.objects.get(id=case_id)
            api_cases = {}
            api_cases['url'] = api_case.url
            api_cases['method'] = api_case.method
            api_cases['header'] = api_case.header
            api_cases['req_type'] = api_case.req_type
            api_cases['req_body'] = api_case.req_body
            api_cases['assert_type'] = api_case.assert_type
            api_cases['assert_body'] = api_case.assert_body
            api_cases['assert_result'] = api_case.assert_result
            api_cases['response_result'] = api_case.response_result
            api_info_data[api_case.name] = api_cases

        # 2、将用例信息，写入到文件当中task_data.json文件当中
        with open(TASK_DATA, 'w', encoding='utf-8') as f:
            f.write(json.dumps(api_info_data))

        # 3、运行文件
        print('运行的任务文件', TASK_RUN)
        os.system("python " + TASK_RUN)
        sleep(2)

        # 4、保存结果
        self.save_result()

        # 5、将状态改为已完成
        task.status = 2
        task.save()

    def save_result(self):
        # 获取task_results的结果
        file = open(TASK_RESULT, encoding='utf-8')
        result_xml = file.read()
        file.close()

        # 提取测试报告的信息
        tree = ElementTree.parse(TASK_RESULT)
        root = tree.getroot()
        info = root.find("testsuite")
        errors, failures, name, skipped, tests, time = info.attrib['errors'], info.attrib['failures'], \
                                                       info.attrib['name'], \
                                                       info.attrib['skipped'], \
                                                       info.attrib['tests'], info.attrib['time']

        # 将结果写入到数据库里面
        TestReport.objects.create(task_id=self.task_id,
                                   name=name,
                                   failures=failures,
                                   errors=errors,
                                   skipped=skipped,
                                   tests=tests,
                                   time=time,
                                   result=result_xml)

    def run_task_thread(self):
        sleep(2)
        t = threading.Thread(target=self.run_task)
        t.start()
        t.join()

    def run(self):
        t1 = threading.Thread(target=self.run_task_thread)
        t1.start()