from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Package, Booking, PackageImage
from .forms import PackageForm, BookingForm
from django.utils import timezone
from django.http import HttpResponseForbidden


def package_list(request):
    packages = Package.objects.filter(status=Package.APPROVED).order_by('-created_at')
    return render(request, 'package_list.html', {'packages': packages})


@login_required
def create_package(request):
    if not request.user.is_vendor:
        messages.error(request, "Only vendors can create packages.")
        return redirect('home')

    if request.method == 'POST':
        form = PackageForm(request.POST, request.FILES)  # ✅ FILES are already passed here

        if form.is_valid():
            package = form.save(commit=False)
            package.vendor = request.user
            package.save()

            # ✅ Handle additional images after main package is saved
            if 'images' in request.FILES:
                for img in request.FILES.getlist('images'):
                    PackageImage.objects.create(package=package, image=img)
                    print(f"Created PackageImage for package {package.id}")

            messages.success(request, "Package created successfully and waiting for admin approval.")
            return redirect('vendor_dashboard')
        else:
            print("Form errors:", form.errors)  # Debug form errors
    else:
        form = PackageForm()

    return render(request, 'create_package.html', {'form': form})


@login_required
def vendor_dashboard(request):
    if not request.user.is_vendor:
        messages.error(request, "Only vendors can access this page.")
        return redirect('home')

    packages = Package.objects.filter(vendor=request.user)
    return render(request, 'vendor_dashboard.html', {'packages': packages})


@login_required
def edit_package(request, pk):
    package = get_object_or_404(Package, pk=pk, vendor=request.user)

    if request.method == 'POST':
        form = PackageForm(request.POST, request.FILES, instance=package)
        if form.is_valid():
            updated_package = form.save(commit=False)
            updated_package.status = Package.PENDING  # Reset status to pending after edit
            updated_package.save()

            # ✅ Handle additional images for edit too
            if 'images' in request.FILES:
                for img in request.FILES.getlist('images'):
                    PackageImage.objects.create(package=updated_package, image=img)

            messages.success(request, "Package updated successfully and waiting for admin approval.")
            return redirect('vendor_dashboard')
    else:
        form = PackageForm(instance=package)

    return render(request, 'edit_package.html', {'form': form, 'package': package})


@login_required
def delete_package(request, pk):
    package = get_object_or_404(Package, pk=pk, vendor=request.user)

    if request.method == 'POST':
        package.delete()
        messages.success(request, "Package has been deleted successfully.")
        return redirect('vendor_dashboard')

    return render(request, 'confirm_delete.html', {'package': package})


@login_required
def vendor_bookings(request, package_id):
    if not request.user.is_vendor:
        return HttpResponseForbidden()

    package = get_object_or_404(Package, pk=package_id, vendor=request.user)
    bookings = Booking.objects.filter(package=package).select_related('user')

    return render(request, 'vendor_bookings.html', {
        'package': package,
        'bookings': bookings
    })


def package_detail(request, pk):
    package = get_object_or_404(Package, pk=pk)
    return render(request, 'package_detail.html', {
        'package': package,
        'images': package.get_images()
    })


# Booking views
@login_required
def create_booking(request, package_id):
    package = get_object_or_404(Package, pk=package_id, status=Package.APPROVED)

    if not package.is_active:
        messages.error(request, "This package is not available for booking.")
        return redirect('package_list')

    if request.method == 'POST':
        form = BookingForm(request.POST, user=request.user, package=package)
        if form.is_valid():
            booking = form.save()
            messages.success(request, "Your booking has been created successfully!")

    else:
        form = BookingForm(user=request.user, package=package)

    return render(request, 'create_booking.html', {
        'form': form,
        'package': package
    })



@login_required
def user_dashboard(request):
    bookings = Booking.objects.filter(user=request.user).order_by('-booking_date')
    return render(request, 'customer_dashboard.html', {'bookings': bookings})


@login_required
def cancel_booking(request, booking_id):
    booking = get_object_or_404(Booking, pk=booking_id, user=request.user)

    if booking.status not in [Booking.PENDING, Booking.CONFIRMED]:
        messages.error(request, "This booking cannot be cancelled.")
        return redirect('user_dashboard')

    if request.method == 'POST':
        booking.status = Booking.CANCELLED
        booking.save()
        messages.success(request, "Your booking has been cancelled.")
        return redirect('user_dashboard')

    return render(request, 'confirm_cancel.html', {'booking': booking})


@login_required
def logout(request):
    return render(request, 'hpg.html')


