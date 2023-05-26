from service.models import Mailing, Client, Message
from django.dispatch import receiver
from django.db.models.signals import post_save, pre_save

from service.utils import send_massages


@receiver(pre_save, sender=Mailing)
def del_message(instance, **kwargs):
    # перед обновлением будут удаляться старые, при условии, что сообщения не были отпралены
    old_mailing = Mailing.objects.filter(id=instance.pk).first()
    if (old_mailing is not None) and (not old_mailing.need_to_send):
        Message.objects.filter(mailing_id=instance.pk).delete()

@receiver(post_save, sender=Mailing)
def signal_message(sender, instance, created, **kwargs):
    # при обновлении(изменении тега, кода, текста) и создании рассылки будут создаваться новые сообщения
    clients = Client.objects.filter(mobile_code=instance.mobile_code, tag=instance.tag)
    for client in clients:
        Message.objects.create(status="waiting", client_id=client.id, mailing_id=instance.id)
    # send_massages(instance.id)


