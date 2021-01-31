from django import forms
from .models import Item, OrderItem, Address


class NewsModal(forms.ModelForm):
    class Meta:
        model = Item
        fields = '__all__'


class ItemForm(forms.ModelForm):
    class Meta:
        model = OrderItem
        fields = ('quantity',)

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
        exclude = ('user',)

    def __init__(self, *args, **kwargs):
        super(CheckoutForm, self).__init__(*args, **kwargs)

        self.fields['first_name'].widget.attrs['class'] = 'form-control'
        self.fields['last_name'].widget.attrs['class'] = 'form-control'
        self.fields['town'].widget.attrs['class'] = 'form-control'
        self.fields['street_address'].widget.attrs['class'] = 'form-control'
        self.fields['street_address'].widget.attrs['placeholder'] = 'Улица и номер'
        self.fields['apartment_address'].widget.attrs['class'] = 'form-control'
        self.fields['apartment_address'].widget.attrs['placeholder'] = 'Апартамент ... (не задължително)'
        self.fields['country'].widget.attrs['class'] = 'form-control'
        self.fields['zip'].widget.attrs['class'] = 'form-control'
        self.fields['phone'].widget.attrs['class'] = 'form-control'
        self.fields['email'].widget.attrs['class'] = 'form-control'
        self.fields['default'].widget.attrs['class'] = 'mr-2'
        self.fields['default'].widget.attrs['type'] = 'checkbox'
