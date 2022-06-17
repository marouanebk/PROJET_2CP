from django import forms
from .models import history


class ordoForm(forms.ModelForm):
    class Meta:
        model = history
        fields = ['diagnostique','lettre','observation']


