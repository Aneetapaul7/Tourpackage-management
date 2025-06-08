from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import ContactForm
from .models import Destination


def hpg(request):
    # Create an empty form for GET requests
    form = ContactForm()
    destinations = Destination.objects.filter(is_active=True).order_by('name')
    return render(request, 'hpg.html', {'form': form,  'destinations': destinations })


def contact_view(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Your message has been sent successfully!')
            return redirect('contact')
    else:
        form = ContactForm()

    return render(request, 'hpg.html', {'form': form})

def destinations_view(request):
    destinations = Destination.objects.filter(is_active=True).order_by('name')
    return render(request, 'destinations.html', {
        'destinations': destinations
    })