from django import forms
from django.core.exceptions import ValidationError

class CheckOutForm(forms.Form):
	address = forms.CharField()
	phone = forms.IntegerField()

	def clean_phone(self):
		data = self.cleaned_data['phone']

		if data > 0:
			return data 

		raise ValidationError('phone is invalid')