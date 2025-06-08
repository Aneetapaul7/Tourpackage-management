from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import CustomUser, Vendor


class CustomUserCreationForm(UserCreationForm):
    first_name = forms.CharField(
        required=True,
        widget=forms.TextInput(attrs={'placeholder': 'First Name'})
    )
    last_name = forms.CharField(
        required=True,
        widget=forms.TextInput(attrs={'placeholder': 'Last Name'})
    )
    phone_number = forms.CharField(
        required=True,
        max_length=15,
        widget=forms.TextInput(attrs={'placeholder': 'Phone Number'})
    )
    email = forms.EmailField(
        required=True,
        widget=forms.EmailInput(attrs={'placeholder': 'Email'})
    )
    user_type = forms.ChoiceField(
        choices=CustomUser.USER_TYPE_CHOICES,
        widget=forms.RadioSelect,
        initial='customer'
    )

    class Meta:
        model = CustomUser
        fields = ['username', 'email', 'first_name', 'last_name',
                  'phone_number', 'password1', 'password2', 'user_type']


class VendorForm(forms.ModelForm):
    company_name = forms.CharField(
        required=True,
        widget=forms.TextInput(attrs={'placeholder': 'Company Name'})
    )

    class Meta:
        model = Vendor
        fields = ['company_name']