from django import forms
from .models import Item, OrderItem, Address


class NewsModal(forms.ModelForm):
	class Meta:
		model = Item
		fields = '__all__'


class ItemForm(forms.Form):
	class Meta:
		item = OrderItem
		fields = ('quantity', )


class CheckoutForm(forms.ModelForm):
	class Meta:
		model = Address
		exclude = ('user', )
