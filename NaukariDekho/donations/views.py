import qrcode

from io import BytesIO

from django.core.files import File

from django.shortcuts import render, redirect, get_object_or_404

from django.utils import timezone

from .forms import DonationForm

from .models import Donation


# YOUR REAL UPI ID
UPI_ID = '6203116265-2@ybl'


# ================= DONATE PAGE =================

def donate(request):

    if request.method == 'POST':

        form = DonationForm(request.POST)

        if form.is_valid():

            donation = form.save()

            # Dynamic UPI Payment Link
            upi_link = (

                f'upi://pay?pa={UPI_ID}'
                f'&pn=NaukriDekho'
                f'&am={donation.amount}'
                f'&cu=INR'

            )

            # Generate QR Code
            qr = qrcode.make(upi_link)

            buffer = BytesIO()

            qr.save(buffer, format='PNG')

            file_name = f'donation_{donation.id}.png'

            donation.qr_code.save(
                file_name,
                File(buffer),
                save=True
            )

            return redirect(
                'donation_qr',
                donation.id
            )

    else:

        form = DonationForm()

    return render(
        request,
        'donations/donate.html',
        {
            'form': form
        }
    )


# ================= QR PAGE =================

def donation_qr(request, donation_id):

    donation = get_object_or_404(
        Donation,
        id=donation_id
    )

    expired = timezone.now() > donation.expires_at

    return render(
        request,
        'donations/donation_qr.html',
        {
            'donation': donation,
            'expired': expired
        }
    )

# ================= CONFIRM PAYMENT =================

def confirm_payment(request, donation_id):

    donation = get_object_or_404(
        Donation,
        id=donation_id
    )

    donation.is_paid = True

    donation.save()

    return redirect('payment_history')

# ================= PAYMENT HISTORY =================

def payment_history(request):

    donations = Donation.objects.filter(
        is_paid=True
    ).order_by('-created_at')

    latest_payment = donations.first()

    return render(
        request,
        'donations/payment_history.html',
        {
            'donations': donations,
            'latest_payment': latest_payment
        }
    )