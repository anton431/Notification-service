from django.dispatch import receiver
from django.db.models.signals import post_save, pre_save

from service.tasks import send_messages
from service.models import Client, Mailing, Message


@receiver(pre_save, sender=Mailing)
def delete_message(instance, **kwargs):
    """
    Перед обновлением будут удаляться старые сообщения,
    при условии, что они не были отпралены
    """
    Message.objects.filter(mailing_id=instance.pk,
                           status=Message.WAITING).delete()


@receiver(post_save, sender=Mailing)
def update_message(sender, instance, created, **kwargs):
    """
    При обновлении(изменении тега, кода, текста)
    и создании рассылки будут создаваться новые сообщения
    """
    clients = Client.objects.filter(mobile_code=instance.mobile_code,
                                    tag=instance.tag)
    client_mesage = dict()

    for client in clients:
        mesage = Message.objects.create(status=Message.WAITING,
                                        client_id=client.pk,
                                        mailing_id=instance.pk)
        client_mesage[client.id] = mesage.pk

    send_messages.apply_async((instance.id, client_mesage),
                              eta=instance.launch_data,
                              expires=instance.end_data)
