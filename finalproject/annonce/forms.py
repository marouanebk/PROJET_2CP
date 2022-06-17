from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate

from .models import forum


class Annonce(forms.ModelForm):
    class Meta:
        model = forum
        fields = ('Author','title','f_description','status',)




	

	
















