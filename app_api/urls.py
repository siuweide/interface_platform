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
    # 保存接口
    path('save_api/', views.save_api, name='save_api'),
    # 编辑接口
    path('edit_api/<int:aid>/', views.edit_api, name='edit_api'),
    # 删除接口
    path('delete_api/', views.delete_api, name='delete_api'),
    # 获取某一条接口信息
    path('get_api_info/', views.get_api_info, name='get_api_info'),
    # 获取项目和模块的数据
    path('get_select_data/', views.get_select_data, name='get_select_data'),
]