from django.contrib import admin
from .models import Message, Client, Mailing


class MailingAdmin(admin.ModelAdmin):
    list_display = ('id', 'launch_data', 'end_data', 'tag', 'mobile_code')
    list_display_links = ('id',)
    search_fields = ('tag', 'mobile_code')
    list_filter = ('tag', 'mobile_code')

class ClientAdmin(admin.ModelAdmin):
    list_display = ('id', 'mobile_code', 'phone', 'tag', 'timezone')
    list_display_links = ('id', 'phone')

class MessageAdmin(admin.ModelAdmin):
    list_display = ('id', 'date_creation', 'status', 'mailing', 'client')
    list_display_links = ('id',)

admin.site.register(Mailing, MailingAdmin)
admin.site.register(Client, ClientAdmin)
admin.site.register(Message, MessageAdmin)
