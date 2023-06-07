from django.dispatch import receiver
from django.db.models.signals import post_save, pre_save

from service.tasks import send_messages
from service.models import Client, Mailing, Message


@receiver(pre_save, sender=Mailing)
def delete_message(instance, **kwargs):
    """
    Old messages will be deleted before the update,
    provided they have not been sent.
    """
    Message.objects.filter(mailing_id=instance.pk,
                           status=Message.WAITING).delete()


@receiver(post_save, sender=Mailing)
def update_message(sender, instance, created, **kwargs):
    """
    When updating (changing the tag, code, text)
    and creating a mailing list, new messages will be created.
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
