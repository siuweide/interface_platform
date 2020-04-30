from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.http import HttpResponse
from django.shortcuts import render, redirect

from app_module.form import ModulesForm
from app_module.models import Module


def module_list(request):
    """ 查询所有模块列表 """
    module_list = Module.objects.all()
    p = Paginator(module_list, 5)
    page = request.GET.get('page', '')
    if page == "":
        page = 1
    try:
        module_list = p.page(page)
    except EmptyPage:
        module_list = p.page(p.num_pages)
    except PageNotAnInteger:
        module_list = p.page(1)
    return render(request, 'module/list.html', {
        "module_list" : module_list
    })

def module_add(request):
    """ 创建模块 """
    if request.method == "GET":
        form = ModulesForm()
    elif request.method == "POST":
        form = ModulesForm(request.POST)
        if form.is_valid():
            # 三种创建方法：
            # 1、
            # project = form.cleaned_data['project']
            # name = form.cleaned_data['name']
            # describe = form.cleaned_data['describe']
            # Module.objects.create(project=project, name=name, describe=describe)
            # 2、
            # Module.objects.create(**form.cleaned_data)
            # 3、
            form.save()
            return redirect('app_module:module_list')
    return render(request, 'module/add.html', {
        "form":form
    })

def module_edit(request, mid):
    """ 编辑模块 """
    module = Module.objects.get(id=mid)
    if request.method == "GET":
        form = ModulesForm(instance=module)
    elif request.method == "POST":
        form = ModulesForm(data=request.POST, instance=module)
        if form.is_valid():
            form.save()
            return redirect('app_module:module_list')
    return render(request, 'module/edit.html', {
        "form":form,
        "id":mid
    })

def module_delete(request):
    """ 删除模块 """
    if request.method == "POST":
        mid = request.POST.get("mid", "")
        if mid:
            module = Module.objects.get(id=mid)
            module.delete()
            return HttpResponse('删除模块成功')
