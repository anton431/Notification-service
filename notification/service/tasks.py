import logging
import os
import requests
from celery.exceptions import SoftTimeLimitExceeded
from celery.worker.control import revoke

from notification.celery import app
from service.models import Mailing, Client, Message

header = {
            "Authorization": "Bearer {}".format(os.getenv("TOKEN")),
            "Content-Type": "application/json",
        }

@app.task
def send_messages(mailing_id, data_set):
    mailing = Mailing.objects.filter(id=mailing_id).first() # для проверки, что рассылка еще не удалена или не изменена
    msgs = Message.objects.filter(mailing_id=mailing_id, status='waiting') # для проверки что таска не старая
    actual_msgs_id = {msg.id for msg in msgs}
    msgs_id = (set(data_set.values()))
    print('Выполняется')
    if mailing and actual_msgs_id == msgs_id: # если рассылка существует и таска не старая
        print('mailing существует')
        clients = Client.objects.filter(mobile_code=mailing.mobile_code, tag=mailing.tag)
        for client in clients:
            if f'{client.id}' in data_set: # сообщение не отправлено
                mesage_id = data_set[f'{client.id}']
                data = {"id": mesage_id, "phone": int(client.phone), "text": mailing.text}
                try:
                    response = requests.post(url=f'https://probe.fbrq.cloud/v1/send/{mesage_id}', headers=header, json=data, timeout=5)
                    print(response)
                    if response.json() == {'code': 0, 'message': 'OK'} and response.ok:
                        del data_set[f'{client.id}'] # сообщение отправлено, удалил
                        Message.objects.filter(id=mesage_id).update(status='sent')
                except Exception as ex:
                    logging.info(repr(ex))
        if data_set:
            return send_messages.apply_async((mailing_id, data_set), countdown=60)

    else:
        print(f'Рассылка {mailing_id} не существует или обновлена')
        return f'Рассылка {mailing_id} не существует или обновлена'
