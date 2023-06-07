from django.db.models import Count
from rest_framework import generics

from service.models import Mailing, Client
from service.serializers import (
    MailingSerializer, ClientSerializer,
    MailingRetrieveSerializer, MailingListSerializer
)


class MailingDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    '''
    get: Viewing the attributes of the updated/deleted mailing list.
    patch: Mailing list attribute updates.
    put: Mailing list attribute updates.
    delete: Deleting a mailing list.
    '''
    queryset = Mailing.objects.all()
    serializer_class = MailingSerializer


class MailingCreateAPIView(generics.CreateAPIView):
    '''
    Adding a new mailing list with all its attributes.
    '''
    queryset = Mailing.objects.all()
    serializer_class = MailingSerializer


class ClientDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    '''
    get: Viewing attributes of the client being updated/deleted.
    patch: Client attribute updates.
    put: Client attribute updates.
    delete: Removing a client from the directory.
    '''
    queryset = Client.objects.all()
    serializer_class = ClientSerializer


class ClientCreateAPIView(generics.CreateAPIView):
    '''
    Adding a new client to the directory with all its attributes.
    '''
    queryset = Client.objects.all()
    serializer_class = ClientSerializer


class MailingRetrieveAPIView(generics.RetrieveAPIView):
    '''
    Getting detailed statistics of sent messages
    on a specific mailing list.
    '''
    queryset = Mailing.objects.all()
    serializer_class = MailingRetrieveSerializer


class MailingListAPIView(generics.ListAPIView):
    '''
    Getting general statistics on created mailings
    the number of messages sent on them, grouped by status.
    '''
    queryset = Mailing.objects.annotate(total_messeges=Count('messages'))
    serializer_class = MailingListSerializer
