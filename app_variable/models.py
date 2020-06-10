from django.db import models
from app_api.models import ApiCase
# Create your models here.

class Variable(models.Model):
    api = models.ForeignKey(ApiCase, on_delete=models.CASCADE, null=True)
    key = models.CharField('键', max_length=255, null=True)
    extract_value = models.CharField('提取值', max_length=255, null=True, default="")
    value = models.CharField('值', max_length=255, null=True)
    describe = models.CharField('描述', max_length=255, default="")
    create_time = models.DateTimeField('创建时间', auto_now_add=True)