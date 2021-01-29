from django import forms
from .models import Item, OrderItem, Address


class NewsModal(forms.ModelForm):
	class Meta:
		model = Item
		fields = '__all__'


class ItemForm(forms.ModelForm):
	class Meta:
		model = OrderItem
		fields = ('quantity', )

	def __init__(self, *args, **kwargs):
		super(ItemForm, self).__init__(*args, **kwargs)

		self.fields['quantity'].widget.attrs['class'] = 'form-control input-number'
		self.fields['quantity'].widget.attrs['type'] = 'text'
		self.fields['quantity'].widget.attrs['id'] = 'quantity'
		self.fields['quantity'].widget.attrs['value'] = '1'
		self.fields['quantity'].widget.attrs['min'] = '1'
		self.fields['quantity'].widget.attrs['max'] = '100'
		self.fields['quantity'].label = ""


class CheckoutForm(forms.ModelForm):
	class Meta:
		model = Address
		exclude = ('user', )

