from django.urls import path

from app_module import views

app_name = 'app_module'
urlpatterns = [
    path('list/', views.module_list, name="module_list"),
    path('add/', views.module_add, name="module_add"),
    path('edit/<int:mid>/', views.module_edit, name="module_edit"),
    path('delete/', views.module_delete, name="module_delete"),
]