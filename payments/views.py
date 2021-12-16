from django.contrib import auth
from django.http import HttpResponseRedirect, HttpResponse
from rest_framework import generics, status, permissions
from rest_framework.response import Response

from users.models import User
from .serializers import PaymentListSerializer, PaymentDetailSerializer, PaymentCreateSerializer
from .models import Payment

from .utils import get_payment_redirect_uri


# Get All Payments made
class PaymentListAPIView(generics.ListAPIView):
    serializer_class = PaymentListSerializer
    queryset = Payment.objects.all()


# Get details of each payment made wrt transaction reference
class PaymentDetailView(generics.GenericAPIView):
    serializer_class = PaymentDetailSerializer

    def get(self, request, ref):
        obj = Payment.objects.filter(trans_ref=ref).last()
        if obj:
            return Response(self.serializer_class(obj).data)
        return Response(f"Oops, No Payment with ref of {ref}", status=status.HTTP_404_NOT_FOUND)


# This will be used to activate the premium package by initiating a payment process
class PaymentCreateAPIView(generics.CreateAPIView):
    serializer_class = PaymentCreateSerializer
    permission_classes = [permissions.AllowAny]

    def post(self, request, *args, **kwargs):
        super(PaymentCreateAPIView, self).post(request, *args, **kwargs)
        print(request.data)
        user_id = request.data["user"]
        demo_user, _ = User.objects.get_or_create(id=user_id)
        auth.login(request, user=demo_user)  # Automatically authenticate, just avoiding manual log in
        url = get_payment_redirect_uri(demo_user)
        return HttpResponseRedirect(url)


# Payments callback where we will grab the transaction_id and status from flutterwave
def status_ipn(request, *args, **kwargs):
    transaction_status = request.GET.get("status")
    transaction_ref = request.GET.get("tx_ref")
    transaction_id = request.GET.get("transaction_id")
    payment = Payment.objects.filter(user=request.user).last()
    payment.trans_ref = transaction_ref
    payment.trans_id = transaction_id
    payment.status = transaction_status  # Flutterwave may delay with the status so a cron job will periodically check
    payment.save()
    return HttpResponse('You payment was processed. We will verify and send you a receipt shortly.')
