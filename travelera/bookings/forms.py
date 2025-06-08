from django import forms
from .models import Booking
from django.utils import timezone


class BookingForm(forms.ModelForm):
    class Meta:
        model = Booking
        fields = ['travel_date', 'number_of_people', 'special_requests']
        widgets = {
            'travel_date': forms.DateInput(attrs={'type': 'date'}),
        }

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)
        self.package = kwargs.pop('package', None)
        super().__init__(*args, **kwargs)

    def clean_travel_date(self):
        travel_date = self.cleaned_data['travel_date']
        if travel_date < timezone.now().date():
            raise forms.ValidationError("Travel date cannot be in the past.")
        return travel_date

    def save(self, commit=True):
        instance = super().save(commit=False)
        if self.user:
            instance.user = self.user
        if self.package:
            instance.package = self.package
            instance.total_price = self.package.price * self.cleaned_data['number_of_people']
        if commit:
            instance.save()
        return instance