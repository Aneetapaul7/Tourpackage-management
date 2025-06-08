from django import forms
from .models import ContactMessage

class ContactForm(forms.ModelForm):
    class Meta:
        model = ContactMessage
        fields = ['name', 'email', 'subject', 'message']
        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'form-control border-black',
                'placeholder': 'Enter your name'
            }),
            'email': forms.EmailInput(attrs={
                'class': 'form-control border-black',
                'placeholder': 'Enter email address'
            }),
            'subject': forms.TextInput(attrs={
                'class': 'form-control border-black',
                'placeholder': 'Enter your subject'
            }),
            'message': forms.Textarea(attrs={
                'class': 'form-control border-black',
                'placeholder': 'Enter your message',
                'rows': 5
            })
        }