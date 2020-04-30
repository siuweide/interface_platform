from django.http import HttpResponse
from django.shortcuts import render

# Create your views here.
from app_api.models import ApiCase


def api_list(request):
    api_list = ApiCase.objects.all()
    return render(request, 'api/list.html', {
        "api_list":api_list
    })

def api_add(request):
    return render(request, 'api/add.html', {

    })

