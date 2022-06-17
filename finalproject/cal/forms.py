import imp
from django.forms import ModelForm, DateInput
from cal.models import RDV
from django import forms
class RDVForm(ModelForm):
    class Meta:
        model = RDV
        fields = ["Sender","Receiver","description", "start_time", "is_approved"]
        # datetime-local is a HTML5 input type
        widgets = {
            "description": forms.Textarea(
                attrs={
                    "class": "form-control",
                    "placeholder": "Enter event description",
                }
            ),
            "start_time": DateInput(
                attrs={"type": "datetime-local", "class": "form-control"},
                format="%Y-%m-%dT%H:%M",
            ),
        }
        exclude = ["user"]

    def __init__(self, *args, **kwargs):
        super(RDVForm, self).__init__(*args, **kwargs)
        # input_formats to parse HTML5 datetime-local input to datetime field
        self.fields["start_time"].input_formats = ("%Y-%m-%dT%H:%M",)

        
# class SecondForm(ModelForm):
#     class Meta:
#         model = RDVForm
#         fields = ["is_approved"]

