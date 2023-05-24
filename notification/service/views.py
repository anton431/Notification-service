from django.shortcuts import render
from rest_framework import generics

from service.models import Mailing
from service.serializers import MailingSerializer


class MailingAPIView(generics.ListAPIView):
    queryset = Mailing.objects.all()
    serializer_class = MailingSerializer

