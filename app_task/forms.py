from django import forms
from django.forms import ModelForm
from app_variable.models import Variable


class VariableForms(ModelForm):
    """ 变量表单 """
    class Meta:
        model = Variable
        fields = ['key', 'value', 'describe']
        widgets = {
            'key':forms.TextInput(attrs={"class":"form-control"}),
            'value':forms.TextInput(attrs={"class":"form-control"}),
            'describe':forms.Textarea(attrs={"class":"form-control"})
        }
