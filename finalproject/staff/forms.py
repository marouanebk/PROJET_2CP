import imp
from django.forms import ModelForm, DateInput
from .models import request_doc
from django import forms
class request_docForm(ModelForm):
    class Meta:
        model = request_doc
        fields = ["owner","speciality","description", "location"]
        # widgets= {
        #     "user": forms.CharField(
        #         attrs={
        #         "class":"numero-tel",
        #                 }
        #                 )
        #     }
        # datetime-local is a HTML5 input type