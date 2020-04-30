from django.core.paginator import Paginator,EmptyPage,PageNotAnInteger
from django.shortcuts import render, redirect

# Create your views here.
from app_project.forms import ProjectForms,ProjectEditForms
from app_project.models import Project


def project_list(request):
    # 项目列表
    project_list = Project.objects.all()
    p = Paginator(project_list, 5)
    page = request.GET.get('page', '')
    if page == "":
        page = 1
    try:
        project_list = p.page(page)
    except PageNotAnInteger:
        project_list = p.page(1)
    except EmptyPage:
        project_list = p.page(p.num_pages)
    return render(request, 'project/list.html', {
        "project_list":project_list
    })

def project_add(request):
    # 项目添加
    if request.method == 'GET':
        form = ProjectForms()
    elif request.method == 'POST':
        form = ProjectForms(request.POST)
        if form.is_valid():
            form.save()
            return redirect('/project/list/')
    return render(request, 'project/add.html', {
        "form":form
    })

def project_edit(request, pid):
    # 项目编辑
    project = Project.objects.get(id=pid)
    if request.method == "GET":
        form = ProjectEditForms(instance=project)
    elif request.method == "POST":
        form = ProjectEditForms(data=request.POST, instance=project)
        if form.is_valid():
            form.save()
            return redirect('app_project:project_list')
    return render(request, 'project/edit.html', {
        "form":form,
        "id":project.id
    })

def project_delete(request):
    """ 项目删除 """
    if request.method == "POST":
        pid = request.POST.get("pid", "")
        project = Project.objects.get(id=pid)
        project.delete()
        return redirect("app_project:project_list")
