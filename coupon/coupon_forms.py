from django import forms
from coupon.models import Coupon

class CouponForm(forms.ModelForm):
	code = forms.CharField(widget=forms.TextInput(attrs={
			'class': 'form-control',
			'placeholder': 'Promo code',
			'aria-label': 'Recipient\'s username',
			'aria-describedby': 'basic-addon2',
			'name' : 'code',
		}))
	class Meta:
		model = Coupon
		fields = ['code']
