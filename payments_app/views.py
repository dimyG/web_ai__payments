from django.shortcuts import render
from rest_framework import viewsets
from .models import Payment
from .serializers import PaymentSerializer
from payments_prj.settings import jwt_secret
from rest_framework.response import Response
from rest_framework.request import Request
from rest_framework import status
from utils.utils import jwt_decode
from .producer import publish_message
import logging

logger = logging.getLogger('payments')


def user_id_from_jwt_in_request(request: Request):
    try:
        decoded_jwt = jwt_decode(request, jwt_secret)
    except Exception as e:
        # not auth header, invalid or expired JWT etc. in all these cases we want to return a 401
        logger.info(f'Exception: {e}')
        return
    user_id = decoded_jwt.get('user_id')
    if not user_id:
        logger.info('No user_id in JWT')
        return
    return user_id


class PaymentMixin(object):
    queryset = Payment.objects.all()
    serializer_class = PaymentSerializer


class PaymentViewSet(PaymentMixin, viewsets.ModelViewSet):
    # define a custom create payment method and add a field to the serializer before it is saved
    # todo: async create and publish
    def create(self, request, *args, **kwargs):
        user_id = user_id_from_jwt_in_request(request)
        if not user_id:
            return Response({'error': 'JWT decoding error!'}, status=status.HTTP_401_UNAUTHORIZED)
        # user_id = 1
        # request.data._mutable = True
        request.data['user_id'] = user_id
        # request.data._mutable = False
        response = super().create(request, *args, **kwargs)
        publish_message(exchange_name='payments', message=response.data)
        return response
