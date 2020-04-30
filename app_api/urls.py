from django.urls import path

from app_api import views

app_name = 'app_api'
urlpatterns = [
    path('list/', views.api_list, name='api_list'),
    path('add/', views.api_add, name='api_add')
]