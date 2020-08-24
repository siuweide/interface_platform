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
    # 任务执行
    path('run/<int:tid>/', views.run_task, name='run_task'),
    # # 任务报告
    # path('report/<int:tid>/', views.task_report, name='task_report'),
    # # 任务详细报告
    # path('report/detail/', views.task_report_detail, name='task_report_detail'),
    # 查看beautifulreport
    path('beautifulreport/<int:tid>/', views.select_beautifulreport, name='select_beautifulreport')
    ]