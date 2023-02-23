from django.shortcuts import render
from rest_framework import viewsets
from .models import Payment
from .serializers import PaymentSerializer


class PaymentMixin(object):
    queryset = Payment.objects.all()
    serializer_class = PaymentSerializer


class PaymentViewSet(PaymentMixin, viewsets.ModelViewSet):
    pass
