import json
from django.http import JsonResponse
from django.shortcuts import render
from django.core.paginator import Paginator,EmptyPage,PageNotAnInteger

# Create your views here.
from app_api.models import ApiCase
from app_module.models import Module
from app_project.models import Project
from app_task.models import Task


def task_list(request):
    # 任务列表
    task_list = Task.objects.all()
    p = Paginator(task_list,5)
    page = request.GET.get("page", "")
    if page == "":
        page = 1
    try:
        task_list = p.page(page)
    except EmptyPage:
        task_list = p.page(p.num_pages)
    except PageNotAnInteger:
        task_list = p.page(1)

    return render(request, 'task/list.html', {
        'task_list':task_list
    })

def task_add(request):
    # 任务添加
    return render(request, 'task/add.html')

def task_save(request):
    # 保存任务
    if request.method == "POST":
        task_id = int(request.POST.get('task_id', ''))
        name = request.POST.get("name", "")
        desc = request.POST.get("desc", "")
        cases_name = request.POST.get("cases", "")
        cases_dict = json.loads(cases_name)
        cases = []
        for name in cases_dict:
            apicase = ApiCase.objects.get(name=name)
            cases.append(apicase.id)
        if task_id == 0:
            Task.objects.create(name=name,
                                describe=desc,
                                cases=cases)
        else:
            task = Task.objects.get(id=task_id)
            task.name = name
            task.describe = desc
            task.cases = cases
            task.save()
        return JsonResponse({"status":10200, "message":"save success"})
    else:
        return JsonResponse({"status": 10201, "message": "request method error"})

def task_edit(request, tid):
    # 编辑任务
    return render(request, 'task/edit.html')

def task_delete(request):
    # 删除任务
    if request.method == 'POST':
        task_id = request.POST.get("task_id", "")
        task = Task.objects.get(id=task_id)
        task.delete()
        return JsonResponse({"status":10200, "message":"delete success"})
    else:
        return JsonResponse({"status": 10201, "message": "request method error"})

def get_case_node(request):
    # 获取用例树
    if request.method == "GET":
        data = []
        project = Project.objects.all()
        mid = 101
        pid = 0
        aid = 1001
        for p in project:
            project_dict = {
                "id":p.id,
                "pid": pid,
                "name":p.name,
                "open":True,
                "isParent":True
            }
            pid += 1
            data.append(project_dict)
            module = Module.objects.filter(project_id=p.id)
            print('mid------------>', mid)
            for m in module:
                print('进入到module------------>')
                module_dict = {
                    "id":mid,
                    "pId":p.id,
                    "name":m.name,
                    "isParent": True
                }
                mid += 1
                data.append(module_dict)
                apicase = ApiCase.objects.filter(module_id=m.id)
                for a in apicase:
                    apicase_dict = {
                        "id":aid,
                        "pId":mid-1,
                        "name":a.name,
                        "isParent": False
                    }
                    aid += 1
                    data.append(apicase_dict)
        return JsonResponse({"status": 10200, "message": "success", "data": data})

    elif request.method == "POST":
        task_id = request.POST.get("task_id", "")
        task = Task.objects.get(id=task_id)
        cases = json.loads(task.cases)
        print('cases----------->', cases)

        task_data = {
            "taskName": task.name,
            "taskDesc": task.describe
        }
        data = []
        project = Project.objects.all()
        mid = 101
        pid = 0
        aid = 1001
        for p in project:
            project_dict = {
                "id":p.id,
                "pid": pid,
                "name":p.name,
                "open":True,
                "isParent":True
            }
            pid += 1
            data.append(project_dict)
            module = Module.objects.filter(project_id=p.id)
            print('mid------------>', mid)
            for m in module:
                print('进入到module------------>')
                module_dict = {
                    "id":mid,
                    "pId":p.id,
                    "name":m.name,
                    "isParent": True
                }
                mid += 1
                data.append(module_dict)
                apicase = ApiCase.objects.filter(module_id=m.id)
                for a in apicase:
                    if a.id in cases:
                        apicase_dict = {
                            "id":aid,
                            "pId":mid-1,
                            "name":a.name,
                            "isParent": False,
                            "checked": True
                        }
                        project_dict['checked'] = True
                        module_dict['checked'] = True
                    else:
                        apicase_dict = {
                            "id":aid,
                            "pId":mid-1,
                            "name":a.name,
                            "isParent": False,
                            "checked": False,
                        }
                    aid += 1
                    data.append(apicase_dict)
        task_data['data'] = data
        return JsonResponse({"status":10200, "message":"success","data":task_data})

def task_run(request):
    # 任务执行
    tid = request.POST.get("task_id", "")
    task = Task.objects.get(id=tid)
    str_cases = task.cases
    case_list = str_cases[1:-1].split(',')
    case_list = [int(x) for x in case_list]
    api_info = {}
    for case_id in case_list:
        api_case = ApiCase.objects.get(id=case_id)
        api_info['name'] = api_case.name