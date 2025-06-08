from django.shortcuts import render, redirect
from django.contrib import messages
from .models import CustomUser, Vendor, Customer
from .forms import CustomUserCreationForm, VendorForm
from django.contrib.auth.decorators import login_required


def register(request):
    if request.method == 'POST':
        user_form = CustomUserCreationForm(request.POST)

        if user_form.is_valid():
            user = user_form.save()

            if user.user_type == 'vendor':
                vendor_form = VendorForm(request.POST)
                if vendor_form.is_valid():
                    vendor = vendor_form.save(commit=False)
                    vendor.user = user
                    vendor.save()
                    messages.success(request, 'Vendor registration successful!')
                else:
                    messages.error(request, 'Invalid vendor details.')
                    return render(request, 'register.html', {
                        'form': user_form,
                        'vendor_form': vendor_form,
                    })
            else:  # Customer
                try:
                    Customer.objects.create(user=user)
                    messages.success(request, 'Customer registration successful!')
                except Exception as e:
                    messages.error(request, f'Error creating customer: {str(e)}')
                    return render(request, 'register.html', {
                        'form': user_form,
                        'vendor_form': VendorForm(),
                    })

            return redirect('login')

        else:  # Form is invalid
            messages.error(request, 'Please correct the errors below.')

    else:  # GET request
        user_form = CustomUserCreationForm()

    return render(request, 'register.html', {
        'form': user_form,
        'vendor_form': VendorForm(),
    })


def login_view(request):
    from django.contrib.auth import authenticate, login
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user:
            login(request, user)
            if user.user_type == 'vendor':
                return redirect('vendor_dashboard')
            else:
                return redirect('customer_dashboard')
    return render(request, 'login.html')


@login_required
def vendor_dashboard(request):
    return render(request, 'vendor_dashboard.html')


@login_required
def customer_dashboard(request):
    return render(request, 'customer_dashboard.html')