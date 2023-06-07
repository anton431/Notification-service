from service.models import Mailing, Client, Message
from django.dispatch import receiver
from django.db.models.signals import post_save, pre_save

from service.tasks import send_messages


@receiver(pre_save, sender=Mailing)
def del_message(instance, **kwargs):
    # перед обновлением будут удаляться старые сообщения, при условии, что они не были отпралены

    Message.objects.filter(mailing_id=instance.pk, status=Message.WAITING).delete()

@receiver(post_save, sender=Mailing)
def signal_message(sender, instance, created, **kwargs):
    # при обновлении(изменении тега, кода, текста) и создании рассылки будут создаваться новые сообщения

    clients = Client.objects.filter(mobile_code=instance.mobile_code, tag=instance.tag)
    data_set = dict()
    for client in clients:
        mesage = Message.objects.create(status=Message.WAITING, client_id=client.pk, mailing_id=instance.pk)
        data_set[client.id] = mesage.pk
    send_messages.apply_async((instance.id, data_set), eta=instance.launch_data, expires=instance.end_data)


