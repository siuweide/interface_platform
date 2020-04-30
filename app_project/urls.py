from django.urls import path

from app_project import views

app_name = 'app_project'
urlpatterns = [
    # 添加项目
    path('list/', views.project_list, name="project_list"),
    path('add/', views.project_add, name="project_add"),
    path('edit/<int:pid>/', views.project_edit, name="project_edit"),
    path('delete/', views.project_delete, name="project_delete")
]