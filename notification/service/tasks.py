import logging
import os
import requests

from notification.celery import app

from service.models import Mailing, Client, Message


header = {
    "Authorization": "Bearer {}".format(os.getenv("TOKEN")),
    "Content-Type": "application/json",
}


@app.task
def send_messages(mailing_id, client_mesage):
    """
    Sends letters to the clients specified in the mailing list.
    """
    # To check that the newsletter has not been deleted or changed yet.
    mailing = Mailing.objects.filter(id=mailing_id).first()
    # To check that the car is not old.
    messages_waiting = Message.objects.filter(mailing_id=mailing_id,
                                              status=Message.WAITING)
    actual_messages_waiting_id = {msg.id for msg in messages_waiting}
    old_messages_waiting_id = set(client_mesage.values())
    # If the mailing list exists and the car is not old.
    if mailing and actual_messages_waiting_id == old_messages_waiting_id:
        clients = Client.objects.filter(mobile_code=mailing.mobile_code,
                                        tag=mailing.tag)

        for client in clients:
            if f'{client.id}' in client_mesage:
                mesage_id = client_mesage[f'{client.id}']
                data = {
                    "id": mesage_id,
                    "phone": int(client.phone),
                    "text": mailing.text
                }

                try:
                    response = requests.post(
                        url=f'https://probe.fbrq.cloud/v1/send/{mesage_id}',
                        headers=header,
                        json=data,
                        timeout=5
                    )
                    if response.json() == {'code': 0, 'message': 'OK'} and response.ok:
                        del client_mesage[f'{client.id}']  # Message sent, deleted
                        Message.objects.filter(id=mesage_id).update(status=Message.SENT)

                except requests.exceptions.RequestException as ex:
                    logging.info(repr(ex))

        if client_mesage:
            return send_messages.apply_async((mailing_id, client_mesage),
                                             countdown=60 * 60)
