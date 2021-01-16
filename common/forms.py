from django import forms
from .models import Item, OrderItem


class NewsModal(forms.ModelForm):
	class Meta:
		model = Item
		fields = '__all__'


class ItemForm(forms.Form):
	class Meta:
		item = OrderItem
		fields = ('quantity', )