from django import forms
from django_countries.fields import CountryField
from django_countries.widgets import CountrySelectWidget


PAYMENT_CHOICES = (
    ('D/C', 'Credit/Debit Card'),
)

default_error_messages = {
    'out_of_range': 'Number must be between 0 and 5.'
}

class CheckoutForm(forms.Form):
    # first_name = forms.CharField(required=False)
    # last_name = forms.CharField(required=False)
    # email = forms.EmailField(required=False)

    # shipping_address = forms.CharField(required=False)
    # shipping_address2 = forms.CharField(required=False)
    # shipping_country = CountryField(blank_label='(select country)').formfield(
    #     required=False,
    #     widget=CountrySelectWidget(attrs={
    #     'class': 'custom-select d-block w-100',
    # }))
    # shipping_zip = forms.CharField(required=False)

    # billing_address = forms.CharField(required=False)
    # billing_address2 = forms.CharField(required=False)
    # billing_country = CountryField(blank_label='(select country)').formfield(
    #     required=False,
    #     widget=CountrySelectWidget(attrs={
    #     'class': 'custom-select d-block w-100',
    # }))
    # billing_postcode = forms.CharField(required=False)
    # same_billing_address = forms.BooleanField(required=False)

    # payment_option = forms.ChoiceField(
    #     widget=forms.RadioSelect, choices=PAYMENT_CHOICES)
    level_of_loyalty = forms.CharField(error_messages=default_error_messages, label='Level of Loyalty (0 <= x >= 5)', widget=forms.TextInput(attrs={'placeholder': '0.00', 'min':0, 'step': '0.01', 'max': 5,'type': 'number'}), required=True)
    merchandise_purchased = forms.CharField(error_messages=default_error_messages, label='Merchandise Purchased (0 <= x >= 5)', widget=forms.NumberInput(attrs={'placeholder': '0.00', 'min':0, 'step': '0.01', 'max': 5,'type': 'number'}), required=True)
    remaining_tickets = forms.CharField(error_messages=default_error_messages, label='Remaining Tickets (0 <= x >= 5)', widget=forms.TextInput(attrs={'placeholder': '0.00', 'min':0, 'step': '0.01', 'max': 5,'type': 'number'}), required=True)

