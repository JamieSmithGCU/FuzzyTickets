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
    level_of_loyalty = forms.CharField(error_messages=default_error_messages, label='Level of Loyalty', widget=forms.TextInput(attrs={'placeholder': '0.00', 'min':0, 'step': '0.01', 'max': 5,'type': 'number'}), required=True, help_text='This field requires a number between 0.00 and 5.00. If you purchase from the same ticket vendor multiple times then you might want to put a number closer to 5. If you have never purchased from a particular vendor before then you might want to pick a number closer to 0. The higher the number, the larger the discount.')
    merchandise_purchased = forms.CharField(error_messages=default_error_messages, label='Amount of Merchandise Purchased', widget=forms.NumberInput(attrs={'placeholder': '0.00', 'min':0, 'step': '0.01', 'max': 5,'type': 'number'}), required=True, help_text='This field requires a number between 0.00 and 5.00. If you frequently support an artist or band by purchasing their merchandise then you might put a number closer to 5, otherwise you might put a number closer to 0.')
    remaining_tickets = forms.CharField(error_messages=default_error_messages, label='Number of Remaining Tickets', widget=forms.TextInput(attrs={'placeholder': '0.00', 'min':0, 'step': '0.01', 'max': 5,'type': 'number'}), required=True, help_text='This field requires a number between 0.00 and 5.00. The number you provide determines how many unsold tickets there are for an event. If the number is closer to 5 then the majority of tickets are available and you would receive a larger discount. If the number is closer to 0, the majority of tickets have already been sold and you would receive a smaller discount.')

