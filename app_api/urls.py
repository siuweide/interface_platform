from django.urls import path

from app_api import views

app_name = 'app_api'
urlpatterns = [
    # 接口列表
    path('list/', views.api_list, name='api_list'),
    # 创建接口
    path('add/', views.api_add, name='api_add'),
    # 发送请求
    path('send_req/', views.send_req, name='send_req'),
    # 获取项目和模块的数据
    path('get_select_data/', views.get_select_data, name='get_select_data'),
    # 保存接口
    path('save_api/', views.save_api, name='get_select_data')
]