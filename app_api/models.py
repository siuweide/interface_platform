from django.db import models

from app_module.models import Module


# Create your models here.

class ApiCaseType(models.Model):
    TYPE_CHOICE = (
        (1, '单接口用例'),
        (2, '多接口业务用例'),
        (3, '公共前置接口用例'),
    )
    type = models.CharField('接口用例类型', max_length=100, choices=TYPE_CHOICE, default=1)
    update_time = models.DateTimeField('更新时间', auto_now=True)
    create_time = models.DateTimeField('创建时间', auto_now_add=True)

class ApiCase(models.Model):
    REQUEST_CHOICE = (
        ('POST', 'POST'),
        ('GET', 'GET'),
        ('PUT', 'PUT'),
        ('DELETE', 'DELETE')
    )
    TYPE_CHOICE = (
        ('FORM-DATA', 'FORM-DATA'),
        ('JSON', 'JSON'),
    )
    ASSERT_CHOICES = (
        ('INCLUDE', 'INCLUDE'),
        ('EQUAL', 'EQUAL')
    )
    COOKIE_CHOICES = (
        ('YES','YES'),
        ('NO','NO')
    )
    """ 接口用例表 """
    module = models.ForeignKey(Module, on_delete=models.CASCADE)
    api_type = models.ForeignKey(ApiCaseType, on_delete=models.CASCADE)
    name = models.CharField('接口名称', max_length=50)
    url = models.CharField('url地址', max_length=500)
    method = models.CharField('请求方式', max_length=100, choices=REQUEST_CHOICE, default='GET')
    is_cookie = models.CharField('是否获取cookie', max_length=50, choices=COOKIE_CHOICES, default='NO')
    header = models.TextField('请求头', blank=True, null=True)
    req_type = models.CharField('参数类型', max_length=50, choices=TYPE_CHOICE, default='FORM-DATA')
    req_body = models.TextField('参数内容', blank=True, null=True)
    assert_type = models.CharField('断言类型', max_length=50, choices=ASSERT_CHOICES, default='INCLUDE')
    assert_body = models.TextField('断言内容',blank=True, null=True)
    assert_result = models.CharField('断言结果', max_length=200,blank=True, null=True)
    response_result = models.TextField('响应结果', blank=True, null=True)
    update_time = models.DateTimeField('更新时间', auto_now=True)
    create_time = models.DateTimeField('创建时间', auto_now_add=True)

    def __str__(self):
        return self.name

    class Meta:
        db_table = 'apicase'
