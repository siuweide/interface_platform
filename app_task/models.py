from django.db import models

# Create your models here.
from app_project.models import Project


class Task(models.Model):
    # 任务表

    STATUS_CHOICES = (
    ('0', '未执行'),
    ('1', '执行中'),
    ('2', '已完成')
    )

    name = models.CharField("名称", max_length=100)
    describe = models.TextField("描述", default="")
    cases = models.TextField("关联用例", default="")
    status = models.SmallIntegerField("状态", default='0', choices=STATUS_CHOICES)
    create_time = models.DateTimeField("创建时间", auto_now_add=True)
    update_time = models.DateTimeField('更改时间', auto_now=True)