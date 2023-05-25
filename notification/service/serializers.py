from rest_framework import serializers
from .models import Mailing, Client


class MailingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Mailing
        fields = ('launch_data', 'end_data', 'text', 'tag', 'mobile_code')

class ClientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Client
        fields = ('phone', 'mobile_code', 'tag', 'timezone')

