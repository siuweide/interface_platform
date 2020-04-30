from django.forms import ModelForm
from django import forms

from app_module.models import Module

class ModulesForm(ModelForm):

    class Meta:
        model = Module
        fields = ['project', 'name', 'describe']
        widgets = {
            'project':forms.Select(attrs={"class":"form-control"}),
            'name':forms.TextInput(attrs={"class":"form-control"}),
            'describe':forms.Textarea(attrs={"class":"form-control"}),
        }

    # def clean_name(self):
    #     name = self.cleaned_data['name']
    #     if name is None:
    #         raise forms.ValidationError('模块名称不能为空')
    #     module_name = Module.objects.filter(name=name)
    #     if module_name:
    #         raise forms.ValidationError('模块名称已存在，请重新输入')
    #     return name