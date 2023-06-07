from rest_framework import serializers

from .models import Mailing, Client


class MailingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Mailing
        fields = ('id', 'launch_data', 'end_data',
                  'text', 'tag', 'mobile_code')


class ClientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Client
        fields = ('id', 'phone', 'mobile_code', 'tag', 'timezone')


class MailingRetrieveSerializer(serializers.ModelSerializer):
    messages = serializers.StringRelatedField(many=True)

    class Meta:
        model = Mailing
        fields = ('id', 'launch_data', 'end_data', 'text',
                  'tag', 'mobile_code', 'messages')


class MailingListSerializer(serializers.ModelSerializer):
    total_messages = serializers.IntegerField()
    total_sent = serializers.IntegerField()

    class Meta:
        model = Mailing
        fields = ('id', 'launch_data', 'end_data', 'text',
                  'tag', 'total_messages', 'total_sent')
