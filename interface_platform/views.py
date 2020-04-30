from django.contrib import auth
from django.contrib.auth import authenticate
from django.http import HttpResponse
from django.shortcuts import render, redirect

def index(request):
    # 首页
    return render(request, 'index.html')

def user_login(request):
    # 用户登录
    if request.method == 'GET':
        return render(request, 'login.html')
    elif request.method == 'POST':
        username = request.POST.get('username', '')
        password = request.POST.get('password', '')
        print('username------->', username)
        print('password------->', password)
        user = authenticate(request,  username=username, password=password )
        if user:
            auth.login(request, user)
            # 第一种方法，登录时设置cookie
            # response = redirect('/index/')
            # response.set_cookie("user", username, 3600)

            # 第二种方法，在index中用{{ user.username }}来展示登录后的名字
            return redirect("app_project:project_list")
        error_message = '用户名或密码错误'
        return render(request, 'login.html', {
            "error_message":error_message
        })

def user_logout(request):
    # 用户退出
    if request.method == 'GET':
        auth.logout(request)
        return HttpResponse('ok')