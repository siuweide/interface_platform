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
    report = models.CharField('关联的测试报告', max_length=100, null=True)
    create_time = models.DateTimeField("创建时间", auto_now_add=True)
    update_time = models.DateTimeField('更改时间', auto_now=True)

    def __str__(self):
        return self.name

# class TestReport(models.Model):
#     # 测试报告表
#     task = models.ForeignKey(Task, on_delete=models.CASCADE)
#     name = models.CharField('用例名称', max_length=255)
#     failures = models.IntegerField('失败用例')
#     errors = models.IntegerField('错误用例')
#     skipped = models.IntegerField('跳过的用例')
#     tests = models.IntegerField('运行总用例数')
#     time = models.FloatField('运行总时长')
#     result = models.TextField("详情", default="")
#     create_time = models.DateTimeField('创建时间', auto_now_add=True)
#
#     def __str__(self):
#         return self.name