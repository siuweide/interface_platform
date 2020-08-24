import json
import re

import requests
from jsonpath_rw import parse
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.http import JsonResponse
from django.shortcuts import render
from django.forms.models import model_to_dict

from app_module.models import Module
from app_project.models import Project
from app_api.models import ApiCase
from app_variable.models import Variable
from util.Assert import Assert

from util.Request import Request


def api_list(request):
    # 接口列表
    api_list = ApiCase.objects.all()
    p = Paginator(api_list, 5)
    page = request.GET.get('page', '')
    if page == "":
        page = 1
    try:
        api_list = p.page(page)
    except EmptyPage:
        api_list = p.page(p.num_pages)
    except PageNotAnInteger:
        api_list = p.page(1)
    return render(request, 'api/list.html', {
        "api_list":api_list
    })

def api_add(request):
    # 创建接口
    return render(request, 'api/add.html', {
    })

def edit_api(request, aid):
    # 编辑接口
    return render(request, 'api/edit.html')

def send_req(request):
    # 发送请求
    if request.method == "POST":
        url = request.POST.get("url", "")
        method = request.POST.get("method", "")
        headers = request.POST.get("headers", "")
        cookie = request.POST.get("cookie", "")
        body = request.POST.get("body", "")
        assert_type = request.POST.get("assert_type", "")
        assert_content = request.POST.get("assert_content", "")
        request = Request()

        if url == "":
            return JsonResponse({"status": 10201, "message":"url is not null"})

        if "${" in url and "}" in url:
            key = re.findall("\${(.+?)}", url)
            variable = Variable.objects.filter(key=key[0])
            if variable:
                for v in variable:
                    url = v.value
            else:
                return JsonResponse({"status": 10202, "message":"variable is not exists"})

        if "${" in headers and "}" in headers:
            headers = request.get_actual_header(headers)

        if "${" in body and "}" in body:
            body = request.get_actual_body(body)

        if method == "GET":
            response = requests.get(url=url, params=json.loads(body), headers=json.loads(headers))
            if cookie == 'yes':
                request.create_or_update_cookie(response)
            response = response.text.encode('utf-8').decode('unicode_escape')
            if assert_content:
                if assert_type == 'include':
                    assert_result_success = Assert().assert_success(assert_content,response)
                    assert_result_fail = Assert().assert_fail(assert_content, response)
                    if assert_result_success:
                        return JsonResponse({"status": 10200, "message": "success", "data": response, "assert":assert_result_success})
                    else:
                        return JsonResponse({"status": 10203, "message": "fail", "data": response, "assert":assert_result_fail})
            else:
                return JsonResponse({"status": 10200, "message": "success", "data": response})

        elif method == "POST":
            response = requests.post(url=url, data=json.loads(body), headers=json.loads(headers))
            if cookie == 'yes':
                request.create_or_update_cookie(response)
            response = response.text.encode('utf-8').decode('unicode_escape')
            if assert_content:
                if assert_type == 'include':
                    assert_result_success = Assert().assert_success(assert_content,response)
                    assert_result_fail = Assert().assert_fail(assert_content, response)
                    if assert_result_success:
                        return JsonResponse({"status": 10200, "message": "success", "data": response, "assert":assert_result_success})
                    else:
                        return JsonResponse({"status": 10204, "message": "fail", "data": response, "assert":assert_result_fail})
            else:
                return JsonResponse({"status": 10200, "message": "success", "data": response})
    else:
        return JsonResponse({"status": 10205, "message":"method error"})

def get_select_data(request):
    # 获取项目、模块的值
    if request.method == "GET":
        data = []
        project = Project.objects.all()
        for p in project:
            project_json = {}
            project_json['id'] = p.id
            project_json['name'] = p.name
            module = Module.objects.filter(project=p.id)
            module_list = []
            for m in module:
                module_json = {}
                module_json['id'] = m.id
                module_json['name'] = m.name
                module_list.append(module_json)
            project_json['moduleList'] = module_list
            data.append(project_json)
        return JsonResponse({"status":10200, "message":"success", "data":data})

def save_api(request):
    # 保存用例
    if request.method == "POST":
        aid = request.POST.get("aid", "")
        name = request.POST.get('name', "")
        url = request.POST.get('url', "")
        method = request.POST.get('method', "")
        headers = request.POST.get('headers', "")
        cookie = request.POST.get("cookie", "")
        par_type = request.POST.get('par_type', "")
        body = request.POST.get('body', "")
        key = request.POST.get("key", "")
        extract_value = request.POST.get("extract_value", "")
        assert_type = request.POST.get('assert_type', "")
        assert_content = request.POST.get("assert_content", "")
        assert_result = request.POST.get("assert_result", "")
        module = request.POST.get('module', "")
        interface_type = request.POST.get("interface_type", "")
        response_result = request.POST.get('response', "")

        if key != "" and extract_value != "":
            response_data = json.loads(response_result)
            json_exe = parse(extract_value)
            madle = json_exe.find(response_data)
            try:
                real_value = [math.value for math in madle][0]
            except IndexError:
                return JsonResponse({"status": 10206, "message": "提取的value值有问题，请检查"})
            variable = Variable.objects.filter(key=key)
            if variable:
                variable[0].extract_value = extract_value
                variable[0].value = real_value
                variable[0].api_id = aid
                variable[0].save()
            else:
                Variable.objects.create(key=key, extract_value=extract_value, value=real_value, api_id=aid)

        if name == "" or url == "" or method == "":
            return JsonResponse({"status":10201, "message":"params error"})

        if aid == "":
            ApiCase.objects.create(name=name,
                                 url=url,
                                 method=method,
                                 header=headers,
                                 req_type=par_type,
                                 req_body=body,
                                 assert_type=assert_type,
                                 assert_body=assert_content,
                                 assert_result=assert_result,
                                 module_id=module,
                                 api_type_id=interface_type,
                                 response_result=response_result,
                                 is_cookie=cookie)
        else:
            apicase = ApiCase.objects.get(id=aid)
            apicase.name = name
            apicase.url = url
            apicase.method = method
            apicase.header = headers
            apicase.req_type = par_type
            apicase.req_body = body
            apicase.assert_type = assert_type
            apicase.assert_body = assert_content
            apicase.assert_result = assert_result
            apicase.response_result = response_result
            apicase.module_id = module
            apicase.api_type_id = interface_type
            apicase.is_cookie = cookie
            apicase.save()
        return JsonResponse({"status":10200, "message":"save api success"})
    else:
        return JsonResponse({"status":10205, "message":"method error"})

def get_api_info(request):
    # 获取接口信息
    if request.method == "GET":
        aid = request.GET.get("aid", "")
        api_case = ApiCase.objects.get(id=aid)
        module = Module.objects.get(id=api_case.module_id)
        project_id = module.project_id
        api_case = model_to_dict(ApiCase.objects.get(id=aid))
        api_case['project_id'] = project_id
        api_variable = Variable.objects.filter(api_id=aid)
        if api_variable:
            for v in api_variable:
                api_key, api_extract_value = v.key, v.extract_value
                api_case['api_key'] = api_key
                api_case['api_extract_value'] = api_extract_value
        return JsonResponse({"status": 10200, "message": "success", "data": api_case})
    else:
        return JsonResponse({"status": 10202, "message": "request method error"})

def delete_api(request):
    # 删除接口
    if request.method == "POST":
        aid = request.POST.get("aid", "")
        try:
            api_case = ApiCase.objects.get(id=aid)
        except ApiCase.DoesNotExist:
            return JsonResponse({"status": 10201, "message": "aid is not exists"})
        api_case.delete()
        return JsonResponse({"status": 10200, "message":"delete success"})
    else:
        return JsonResponse({"status": 10202, "message": "request method error"})