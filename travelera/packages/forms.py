from django import forms
from .models import Package, Booking, PackageImage
from django.utils import timezone
from datetime import timedelta

class MultipleFileInput(forms.ClearableFileInput):
    allow_multiple_selected = True

class MultipleFileField(forms.FileField):
    def __init__(self, *args, **kwargs):
        kwargs.setdefault("widget", MultipleFileInput())
        super().__init__(*args, **kwargs)

    def clean(self, data, initial=None):
        single_file_clean = super().clean
        if isinstance(data, (list, tuple)):
            result = [single_file_clean(d, initial) for d in data]
        else:
            result = single_file_clean(data, initial)
        return result

class PackageForm(forms.ModelForm):
    images = MultipleFileField(required=False, label='Additional Images')

    class Meta:
        model = Package
        fields = ['title', 'description', 'destination', 'price', 'duration_days', 'expiry_date', 'image']
        widgets = {
            'expiry_date': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
        }

    def __init__(self, *args, **kwargs):
        self.vendor = kwargs.pop('vendor', None)
        super().__init__(*args, **kwargs)

    # ✅ Simplified save method - let the view handle image creation
    def save(self, commit=True):
        instance = super().save(commit=False)
        if self.vendor:
            instance.vendor = self.vendor
        if commit:
            instance.save()
        return instance

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