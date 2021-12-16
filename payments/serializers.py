from rest_framework import serializers
from .models import Payment


class PaymentDetailSerializer(serializers.ModelSerializer):

    class Meta:
        model = Payment
        fields = '__all__'


class PaymentListSerializer(serializers.ModelSerializer):

    class Meta:
        model = Payment
        fields = ['trans_ref', 'status']


class PaymentCreateSerializer(serializers.ModelSerializer):

    class Meta:
        model = Payment
        fields = ['user']
