from django import forms
from rdv.models import Rendez_vous


class RendezVousForm(forms.ModelForm):

	class Meta:
		model = Rendez_vous
		fields ='__all__'

		