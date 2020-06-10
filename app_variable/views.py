from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.http import HttpResponse
from django.shortcuts import render, redirect

# Create your views here.
from app_task.forms import VariableForms
from app_variable.models import Variable


def variable_list(request):
    # 变量管理列表
    variable_list = Variable.objects.all()
    p = Paginator(variable_list, 5)
    page = request.GET.get("page", "")
    if page == "":
        page = 1
    try:
        variable_list = p.page(page)
    except EmptyPage:
        variable_list = p.page(p.num_pages)
    except PageNotAnInteger:
        variable_list = p.page(1)
    return render(request, 'variable/list.html', {
        "variable_list":variable_list
    })

def variable_add(request):
    # 添加变量
    if request.method == "POST":
        form = VariableForms(request.POST)
        if form.is_valid():
            key = form.cleaned_data['key']
            value = form.cleaned_data['value']
            describe = form.cleaned_data['describe']
            Variable.objects.create(key=key, value=value, describe=describe)
            return redirect('app_variable:variable_list')
    else:
        form = VariableForms()
    return render(request, 'variable/add.html', {
        "form": form
    })

def variable_edit(request, vid):
    # 修改变量
    variable = Variable.objects.get(id=vid)
    if request.method == "POST":
        form = VariableForms(request.POST, instance=variable)
        if form.is_valid():
            form.save()
            return redirect('app_variable:variable_list')
    elif request.method == "GET":
        form = VariableForms(instance=variable)
    return render(request, 'variable/edit.html', {
        "form": form,
        "id": variable.id
    })

def variable_delete(request):
    # 删除变量
    if request.method == "POST":
        vid = request.POST.get("vid", "")
        variable = Variable.objects.get(id=vid)
        variable.delete()
        return HttpResponse('ok')