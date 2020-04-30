from django import forms
from django.forms import ModelForm
from django.forms import widgets

from app_project.models import Project


class ProjectForms(forms.Form):
    """ 项目表单 """
    name = forms.CharField(label="项目名称",
                           max_length=100,
                           widget=widgets.TextInput(attrs={"class":"form-control"}))
    describe = forms.CharField(label="项目描述",
                               max_length=200,
                               widget=widgets.Textarea(attrs={"class":"form-control"}))
    status = forms.BooleanField(label="状态",
                                required=False,
                                widget=widgets.CheckboxInput())

    def clean_name(self):
        """ 验证项目名称 """
        name = self.cleaned_data['name']
        if name is None:
            raise forms.ValidationError('请输入项目名称')
        project_name = Project.objects.filter(name=name)
        if project_name:
            raise forms.ValidationError('项目名称已存在，请重新输入')
        return name

class ProjectEditForms(ModelForm):
    """ 项目编辑表单 """
    class Meta:
        model = Project
        fields = ['name', 'describe', 'status']
        widgets = {
            'name':forms.TextInput(attrs={"class":"form-control"}),
            'describe':forms.Textarea(attrs={"class":"form-control"})
        }