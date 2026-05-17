from django.urls import path

from . import views


urlpatterns = [

    path(
        'donate/',
        views.donate,
        name='donate'
    ),

    path(
        'donation-qr/<int:donation_id>/',
        views.donation_qr,
        name='donation_qr'
    ),

    path(
    'confirm-payment/<int:donation_id>/',
    views.confirm_payment,
    name='confirm_payment'
),

path(
    'payment-history/',
    views.payment_history,
    name='payment_history'
),

]