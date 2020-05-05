import json
import requests
from django.http import JsonResponse
from django.shortcuts import render

from app_module.models import Module
from app_project.models import Project
from app_api.models import ApiCase
from util.Assert import Assert

# Create your views here.



def api_list(request):
    # 接口列表
    api_list = ApiCase.objects.all()
    return render(request, 'api/list.html', {
        "api_list":api_list
    })

def api_add(request):
    # 创建接口
    return render(request, 'api/add.html', {

    })

def send_req(request):
    # 发送请求
    if request.method == "POST":
        url = request.POST.get("url", "")
        method = request.POST.get("method", "")
        headers = json.loads(request.POST.get("headers", ""))
        body = request.POST.get("body", "")
        assert_type = request.POST.get("assert_type", "")
        assert_content = request.POST.get("assert_content", "")
        print('url------------>',url)
        print('method------------>',method)
        print('headers------------>',headers)
        print('body------------>',body)
        if url == "":
            return JsonResponse({"status": 10201, "message":"url is not null"})
        if method == "GET":
            response = requests.get(url=url, params=body, headers=headers).json()
            if assert_content:
                if assert_type == 'include':
                    assert_result_success = Assert().assert_success(assert_content,response)
                    assert_result_fail = Assert().assert_fail(assert_content, response)
                    if assert_result_success:
                        return JsonResponse({"status": 10200, "message": "success", "data": response, "assert":assert_result_success})
                    else:
                        return JsonResponse({"status": 10201, "message": "fail", "data": response, "assert":assert_result_fail})
            else:
                return JsonResponse({"status": 10200, "message": "success", "data": response})
        elif method == "POST":
            response = requests.post(url=url, data=body, headers=headers).json()
            if assert_content:
                if assert_type == 'include':
                    assert_result_success = Assert().assert_success(assert_content,response)
                    assert_result_fail = Assert().assert_fail(assert_content, response)
                    if assert_result_success:
                        return JsonResponse({"status": 10200, "message": "success", "data": response, "assert":assert_result_success})
                    else:
                        return JsonResponse({"status": 10201, "message": "fail", "data": response, "assert":assert_result_fail})
            else:
                return JsonResponse({"status": 10200, "message": "success", "data": response})
    else:
        return JsonResponse({"status": 10202, "message":"method error"})

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
    if request.method == "POST":
        print("进入到post请求里面")
        name = request.POST.get('name', "")
        url = request.POST.get('url', "")
        method = request.POST.get('method', "")
        headers = json.loads(request.POST.get('headers', ""))
        par_type = request.POST.get('par_type', "")
        body = request.POST.get('body', "")
        assert_type = request.POST.get('assert_type', "")
        assert_content = request.POST.get("assert_content", "")
        assert_result = request.POST.get("assert_result", "")
        module = request.POST.get('module', "")
        print('method------------->',method)
        print('headers------------->',headers)
        print('par_type------------->',par_type)
        print('par_type------------->',par_type)
        print('body------------->',body)

        if name == "" or url == "" or method == "":
            return JsonResponse({"status":10201, "message":"params error"})

        apicase = ApiCase.objects.create(name=name,
                                         url=url,
                                         method=method,
                                         header=headers,
                                         req_type=par_type,
                                         req_body=body,
                                         assert_type=assert_type,
                                         assert_body=assert_content,
                                         assert_result=assert_result,
                                         module_id=module)
        return JsonResponse({"status":10200, "message":"save api success"})
    else:
        return JsonResponse({"status":10205, "message":"method error"})