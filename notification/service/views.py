from django.db.models import Count
from rest_framework import generics
from service.models import Mailing, Client
from service.serializers import MailingSerializer, ClientSerializer, MailingRetrieveSerializer, MailingListSerializer


class MailingDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    '''
    get: Просмотр атрибутов обновляемой/удаляемой рассылки
    patch: Обновления атрибутов рассылки
    put: Обновления атрибутов рассылки
    delete: Удаление рассылки
    '''
    queryset = Mailing.objects.all()
    serializer_class = MailingSerializer


class MailingCreateAPIView(generics.CreateAPIView):
    '''Добавление новой рассылки со всеми её атрибутами'''
    queryset = Mailing.objects.all()
    serializer_class = MailingSerializer


class ClientDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    '''
    get: Просмотр атрибутов обновляемого/удаляемого клиента
    patch: Обновления атрибутов клиента
    put: Обновления атрибутов клиента
    delete: Удаление клиента из справочника
    '''
    queryset = Client.objects.all()
    serializer_class = ClientSerializer


class ClientCreateAPIView(generics.CreateAPIView):
    '''Добавления нового клиента в справочник со всеми его атрибутами'''
    queryset = Client.objects.all()
    serializer_class = ClientSerializer


class MailingRetrieveAPIView(generics.RetrieveAPIView):
    '''
    Получение детальной статистики отправленных сообщений по конкретной рассылке
    '''
    queryset = Mailing.objects.all()
    serializer_class = MailingRetrieveSerializer


class MailingListAPIView(generics.ListAPIView):
    '''
    Получение общей статистики по созданным рассылкам и
    количеству отправленных сообщений по ним с группировкой по статусам
    '''
    queryset = Mailing.objects.annotate(total_messeges=Count('messages'))
    serializer_class = MailingListSerializer
