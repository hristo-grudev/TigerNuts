from django import forms

from accounts.models import Subscribers
from .models import Item, OrderItem, Address

PAYMENT_CHOICES = (
    ('C', 'Наложен платеж (плащане в брой на куриера при доставка)'),
    # ('S', 'С кредитна/дебитна карта онлайн'),
    # ('B', 'Директен банков трансфер')
)

COUNTRY_CHOICES = (
    ('BG', 'България'),
    ('RO', 'Romania'),
    ('GR', 'Greece'),
    ('GR', 'Greece'),
    ('SR', 'Serbia'),
    ('MK', 'North Macedonia'),
)

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


class CheckoutForm(forms.Form):
    first_name = forms.CharField(required=False)
    last_name = forms.CharField(required=False)
    town = forms.CharField(required=False)
    street_address = forms.CharField(required=False)
    apartment_address = forms.CharField(required=False)
    country = forms.ChoiceField(required=False, choices=COUNTRY_CHOICES)
    zip = forms.CharField(required=False)
    phone = forms.CharField(required=False)
    email = forms.CharField(required=False)
    set_default_shipping = forms.BooleanField(required=False)
    payment_option = forms.ChoiceField(
        widget=forms.RadioSelect, choices=PAYMENT_CHOICES)

    def __init__(self, *args, **kwargs):
        super(CheckoutForm, self).__init__(*args, **kwargs)

        self.fields['first_name'].widget.attrs['class'] = 'form-control'
        self.fields['first_name'].widget.attrs['name'] = 'first_name'
        self.fields['last_name'].widget.attrs['class'] = 'form-control'
        self.fields['last_name'].widget.attrs['name'] = 'last_name'
        self.fields['town'].widget.attrs['class'] = 'form-control'
        self.fields['town'].widget.attrs['name'] = 'town'
        self.fields['street_address'].widget.attrs['class'] = 'form-control'
        self.fields['street_address'].widget.attrs['placeholder'] = 'Улица и номер'
        self.fields['street_address'].widget.attrs['name'] = 'street_address'
        self.fields['apartment_address'].widget.attrs['class'] = 'form-control'
        self.fields['apartment_address'].widget.attrs['name'] = 'apartment_address'
        self.fields['apartment_address'].widget.attrs['placeholder'] = 'Апартамент ... (не задължително)'
        self.fields['country'].widget.attrs['class'] = 'form-control'
        self.fields['country'].widget.attrs['name'] = 'country'
        self.fields['zip'].widget.attrs['class'] = 'form-control'
        self.fields['zip'].widget.attrs['name'] = 'zip'
        self.fields['phone'].widget.attrs['class'] = 'form-control'
        self.fields['phone'].widget.attrs['name'] = 'phone'
        self.fields['email'].widget.attrs['class'] = 'form-control'
        self.fields['email'].widget.attrs['name'] = 'email'
        self.fields['set_default_shipping'].widget.attrs['class'] = 'mr-2'
        self.fields['set_default_shipping'].widget.attrs['type'] = 'checkbox'
        self.fields['set_default_shipping'].widget.attrs['name'] = 'set_default_shipping'


class CouponForm(forms.Form):
    code = forms.CharField(widget=forms.TextInput(attrs={
        'class': 'form-control text-left px-3',
        'placeholder': 'Промо код'
    }))


class PaymentForm(forms.Form):
    stripeToken = forms.CharField(required=False)
    save = forms.BooleanField(required=False)
    use_default = forms.BooleanField(required=False)


class SubscriberForm(forms.ModelForm):
    class Meta:
        model = Subscribers
        fields = ('email', )

    def __init__(self, *args, **kwargs):
        super(SubscriberForm, self).__init__(*args, **kwargs)

        self.fields['email'].widget.attrs['class'] = 'form-control'
        self.fields['email'].widget.attrs['placeholder'] = "Въведи e-mail адрес"
        self.fields['email'].widget.attrs['type'] = "text"
        self.fields['email'].label = ''
