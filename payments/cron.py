from .models import Payment


# By default, payment is not set on the table
# We thence loop over only those to check the status and update the payment amount
# Make sure we loop over payments with IDs since those are the complete ones
from .utils import get_payment_details


def validate_status():
    payments = Payment.objects.filter(amount=None, trans_id__isnull=False)
    for payment in payments:
        payment_details = get_payment_details(trans_id=payment.trans_id)
        payment.amount = payment_details["data"]["amount"]
        if payment_details["data"]["status"] != "successful":
            payment.status = payment_details["data"]["status"]
            payment.user.is_premium = False
            # You can choose to invalidate the user account
            # payment.user.is_active = False
        payment.status = payment_details["data"]["status"]
        payment.save()
