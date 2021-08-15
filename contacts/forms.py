from django import forms
from django.forms import ModelForm
from contacts.models import Contact



class ContactForm(ModelForm):

	name = forms.CharField(widget=forms.TextInput(attrs={
				'class' : 'form-control rounded border',
				'id' : 'contact_name',
				'type' : 'text',
				'name' : 'contact_name',
				'placeholder' : 'Your name &/or surname ...',
		}))

	email = forms.EmailField(widget=forms.EmailInput(attrs={
				'class' : 'form-control rounded border',
				'id' : 'contact_email',
				'type' : 'email',
				'placeholder' : 'Your valid email address ...',
				'name' : 'contact_email',
		}))

	subject = forms.CharField(widget=forms.TextInput(attrs={
				'class' : 'form-control rounded border',
				'id' : 'subject',
				'type' : 'text',
				'name' : 'contact_subject',
				'placeholder' : 'Your subject ...',
		}))

	message = forms.CharField(widget=forms.Textarea(
		attrs={
			'class' : 'form-control rounded border md-textarea',
			'rows' : '7',
			'id' : 'message',
			'placeholder' : 'Type your message here ...',
			'required' : 'true',
			'name' : 'contact_message',
		}))
	
	class Meta:
		model = Contact
		fields = ['name', 'email', 'subject', 'message']
