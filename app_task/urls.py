from django.urls import path

from app_task import views

app_name = 'app_task'
urlpatterns = [
    # 任务列表
    path('list/', views.task_list, name='task_list'),
    # 任务添加
    path('add/', views.task_add, name='task_add'),
    # 任务保存
    path('save/', views.task_save, name='task_save'),
    # 任务修改
    path('edit/<int:tid>/', views.task_edit, name='task_edit'),
    # 任务删除
    path('delete/', views.task_delete, name='task_delete'),
    # 获取项目/模块/用例
    path('get_case_node/', views.get_case_node, name='get_case_node'),
    ]