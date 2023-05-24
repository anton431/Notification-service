from rest_framework import serializers
from .models import Mailing


class MailingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Mailing
        fields = ('launch_data', 'end_data', 'text', 'tag', 'mobile_code')

