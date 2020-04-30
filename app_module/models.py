from django.db import models

# Create your models here.
from app_project.models import Project

class Module(models.Model):
    """ 模块表 """
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    name = models.CharField("模块名称", max_length=100)
    describe = models.TextField("描述", default="")
    update_time = models.DateTimeField("更新时间", auto_now=True)
    create_time = models.DateTimeField("创建时间", auto_now_add=True)

    def __str__(self):
        return self.name