from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django import forms
from django.forms import ModelForm, ModelChoiceField
from .models import *
from django.db import transaction
from datetime import datetime

class UserSignupForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = User
        fields = ['username', 'password1', 'password2']
        labels = {
            'password1': 'Password',
            'password2': 'Password confirmation',
        }
        help_texts = {
            'username': None,
            'password1': None,
            'password2': None,
        }

    @transaction.atomic
    def save(self):
        user = super().save(commit=False)
        user.is_admin = False
        user.email = self.cleaned_data['username']
        user.save()
        return user
    
class UserLoginForm(AuthenticationForm):
    def __init__(self, *args, **kwargs):
        super(UserLoginForm, self).__init__(*args, **kwargs)

class PizzaOrder(forms.ModelForm):
    toppings = forms.ModelMultipleChoiceField(
        queryset=Topping.objects.all(),
        widget=forms.CheckboxSelectMultiple,
        required=True
    )
    class Meta:
        model = Pizza
        fields = ['size', 'crust', 'sauce', 'cheese', 'toppings']

class OrderForm(forms.ModelForm):
    expiry_date = forms.CharField(
        widget=forms.TextInput(attrs={'placeholder': 'MM/YY'}),
        label="Expiry Date"
     )

    class Meta:
        model = Order
        fields = ['address', 'card_num', 'expiry_date', 'cvv']

    def clean_expiry_date(self):
        expiry = self.cleaned_data.get('expiry_date')
        
        try:
            exp_month, exp_year = expiry.split('/')
            exp_month = int(exp_month)
            exp_year = int(exp_year) + 2000  # Convert YY to YYYY
            exp_date = datetime(exp_year, exp_month, 1)
        except ValueError:
            raise forms.ValidationError("Invalid date format. Use MM/YY.")

        if exp_date < datetime.today():
            raise forms.ValidationError("Card has expired.")

        return exp_date