from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from packages.models import Package
from .models import Booking
from .forms import BookingForm


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
            return redirect('user_dashboard')
    else:
        form = BookingForm(user=request.user, package=package)

    return render(request, 'create_booking.html', {
        'form': form,
        'package': package
    })


@login_required
def user_dashboard(request):
    bookings = Booking.objects.filter(user=request.user)
    return render(request, 'user_dashboard.html', {'bookings': bookings})


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
def vendor_bookings(request):
    if not request.user.is_vendor:
        messages.error(request, "Only vendors can access this page.")
        return redirect('home')

    bookings = Booking.objects.filter(package__vendor=request.user)
    status_filter = request.GET.get('status')

    if status_filter:
        bookings = bookings.filter(status=status_filter)

    return render(request, 'vendor_bookings.html', {
        'bookings': bookings,
        'status_filter': status_filter
    })


@login_required
def update_booking_status(request, booking_id):
    booking = get_object_or_404(Booking, pk=booking_id, package__vendor=request.user)

    if request.method == 'POST':
        new_status = request.POST.get('status')
        if new_status in [Booking.CONFIRMED, Booking.CANCELLED, Booking.COMPLETED]:
            booking.status = new_status
            booking.save()
            messages.success(request, f"Booking status updated to {booking.get_status_display()}.")
        return redirect('vendor_bookings')

    return render(request, 'update_booking_status.html', {
        'booking': booking,
        'status_choices': [
            (Booking.CONFIRMED, 'Confirmed'),
            (Booking.CANCELLED, 'Cancelled'),
            (Booking.COMPLETED, 'Completed'),
        ]
    })