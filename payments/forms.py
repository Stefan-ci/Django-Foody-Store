from django import forms

class PaymentForm(forms.Form):
	stripeToken = forms.CharField(required=False)
	save = forms.BooleanField(required=False)
	use_default = forms.BooleanField(required=False)
