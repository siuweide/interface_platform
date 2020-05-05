import json
class Assert():

    def assert_success(self, assert_content, response):
        if assert_content in response:
            response = json.loads(response)
            response['assert_result'] = '断言成功，断言内容包含在响应结果里'
            return response['assert_result']
        elif assert_content == response:
            response = json.loads(response)
            response['assert_result'] = '断言成功，断言内容等于响应结果里'
            return response['assert_result']

    def assert_fail(self, assert_content, response):
        if assert_content not in response:
            response = json.loads(response)
            response['assert_result'] = '断言失败，断言内容不包含在响应结果里'
            return response['assert_result']
        elif assert_content == response:
            response = json.loads(response)
            response['assert_result'] = '断言失败，断言内容不等于响应结果里'
            return response['assert_result']