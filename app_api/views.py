import json
import requests
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.http import JsonResponse
from django.shortcuts import render
from django.forms.models import model_to_dict

from app_module.models import Module
from app_project.models import Project
from app_api.models import ApiCase
from util.Assert import Assert

# Create your views here.

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
        headers = json.loads(request.POST.get("headers", ""))
        body = json.loads(request.POST.get("body", ""))
        assert_type = request.POST.get("assert_type", "")
        assert_content = request.POST.get("assert_content", "")
        print('url------------>',url)
        print('method------------>',method)
        print('headers------------>',headers)
        print('body------------>',body)
        if url == "":
            return JsonResponse({"status": 10201, "message":"url is not null"})
        if method == "GET":
            response = requests.get(url=url, params=body, headers=headers,).text
            response = response.encode('utf-8').decode('unicode_escape')
            if assert_content:
                if assert_type == 'include':
                    assert_result_success = Assert().assert_success(assert_content,response)
                    assert_result_fail = Assert().assert_fail(assert_content, response)
                    if assert_result_success:
                        return JsonResponse({"status": 10200, "message": "success", "data": response, "assert":assert_result_success})
                    else:
                        return JsonResponse({"status": 10200, "message": "fail", "data": response, "assert":assert_result_fail})
            else:
                return JsonResponse({"status": 10200, "message": "success", "data": response})
        elif method == "POST":
            response = requests.post(url=url, data=body, headers=headers).text
            response = response.encode('utf-8').decode('unicode_escape')
            if assert_content:
                if assert_type == 'include':
                    assert_result_success = Assert().assert_success(assert_content,response)
                    assert_result_fail = Assert().assert_fail(assert_content, response)
                    if assert_result_success:
                        return JsonResponse({"status": 10200, "message": "success", "data": response, "assert":assert_result_success})
                    else:
                        return JsonResponse({"status": 10200, "message": "fail", "data": response, "assert":assert_result_fail})
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
    # 保存用例
    if request.method == "POST":
        aid = request.POST.get("aid", "")
        name = request.POST.get('name', "")
        url = request.POST.get('url', "")
        method = request.POST.get('method', "")
        headers = request.POST.get('headers', "")
        par_type = request.POST.get('par_type', "")
        body = request.POST.get('body', "")
        assert_type = request.POST.get('assert_type', "")
        assert_content = request.POST.get("assert_content", "")
        assert_result = request.POST.get("assert_result", "")
        module = request.POST.get('module', "")
        response_result = request.POST.get('response', "")
        print('method------------->',method)
        print('headers------------->',headers)
        print('par_type------------->',par_type)
        print('par_type------------->',par_type)
        print('body------------->',body)
        print('response_result------------->',response_result)

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
                                 response_result=response_result)
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