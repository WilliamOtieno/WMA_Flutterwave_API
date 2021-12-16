import requests
import json

from django.shortcuts import reverse
from django.conf import settings
from django.utils.crypto import get_random_string
from .models import Payment
from users.models import User

token = settings.FW_SECRET_KEY


# Generate a random string for the transaction_ref
# If the ref already exists, regenerate the reference
def get_random_ref():
    ref = get_random_string(10)
    if Payment.objects.filter(trans_id=ref).exists():
        ref = get_random_string(10)
    return ref


# Pass in a user in order to generate the uri needed for initiating payment
def get_payment_redirect_uri(user):
    url = "https://api.flutterwave.com/v3/payments"

    payload = json.dumps({
        "tx_ref": f"{get_random_ref()}",
        "amount": "2000",
        "currency": "KES",
        "redirect_url": "http://127.0.0.1:8000/payment-status",
        "payment_options": "mpesa",
        "customer": {
            "email": f"{user.email}",
            "phonenumber": f"{user.phone_number}",
            "name": f"{user.first_name} {user.last_name}"
        },
        "customizations": {
            "title": "WMA Payments",
            "description": "Give Caesar what.....or whatever he said",
        }
    })
    headers = {
        'Authorization': f'Bearer {token}',
        'Content-Type': 'application/json'
    }

    response = requests.request("POST", url, headers=headers, data=payload)
    link = response.json()["data"]["link"]
    return link


def get_payment_details(trans_id):
    url = f"https://api.flutterwave.com/v3/transactions/{trans_id}/verify"

    payload = {}
    headers = {
        'Authorization': f'Bearer {token}'
    }

    response = requests.request("GET", url, headers=headers, data=payload)

    return response.json()
