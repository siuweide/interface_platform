from django.urls import path

from app_variable import views

app_name = 'app_variable'
urlpatterns = [
    # 变量列表
    path('list/', views.variable_list, name='variable_list'),
    # 创建变量
    path('add/', views.variable_add, name='variable_add'),
    # 修改变量
    path('edit/<int:vid>/', views.variable_edit, name='variable_edit'),
    # 删除变量
    path('delete/', views.variable_delete, name='variable_delete'),
]