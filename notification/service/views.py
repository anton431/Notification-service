from rest_framework import generics

from service.models import Mailing, Client
from service.serializers import MailingSerializer, ClientSerializer


class MailingDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Mailing.objects.all()
    serializer_class = MailingSerializer

class MailingCreateAPIView(generics.CreateAPIView):
    queryset = Mailing.objects.all()
    serializer_class = MailingSerializer

class ClientDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Client.objects.all()
    serializer_class = ClientSerializer

class ClientCreateAPIView(generics.CreateAPIView):
    queryset = Client.objects.all()
    serializer_class = ClientSerializer

