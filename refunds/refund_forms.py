from django import forms
from django.forms import ModelForm
from refunds.models import Refund


class RefundForm(forms.Form):
	ref_code = forms.CharField(widget=forms.TextInput(attrs={
				'class' : 'form-control',
				'id' : 'ref_code',
				'type' : 'text',
				'name' : 'ref_code',
				'placeholder' : 'Referral code ...',
		}))
	email = forms.EmailField(widget=forms.EmailInput(attrs={
				'class' : 'form-control',
				'id' : 'email',
				'type' : 'email',
				'placeholder' : 'Your valid email address ...',
				'name' : 'email',
		}))
	message = forms.CharField(widget=forms.Textarea(
		attrs={
			'class' : 'form-control',
			'rows' : '7',
			'id' : 'message',
			'placeholder' : 'Type your reason here ...',
			'required' : 'true',
			'name' : 'reason',
		}))
	
