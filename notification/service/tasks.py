import logging
import os
import requests

from notification.celery import app
from service.models import Mailing, Client, Message


header = {
            "Authorization": "Bearer {}".format(os.getenv("TOKEN")),
            "Content-Type": "application/json",
        }

@app.task(bind=True)
def send_messages(self, mailing_id, data_set):
    mailing = Mailing.objects.filter(id=mailing_id).first() # для проверки, что рассылка еще не удалена или не изменена
    print('Выполняется')
    if mailing: # если рассылка существует
        print('mailing существует')
        clients = Client.objects.filter(mobile_code=mailing.mobile_code, tag=mailing.tag)
        for client in clients:
            if f'{client.id}' in data_set: # сообщение не отправлено
                mesage_id = data_set[f'{client.id}']
                data = {"id": mesage_id, "phone": int(client.phone), "text": mailing.text}
                try:
                    response = requests.post(url=f'https://probe.fbrq.cloud/v1/send/{mesage_id}', headers=header, json=data).json()
                    print(response)
                    print(response.json())
                    if response.json() == {'code': 0, 'message': 'OK'} and response.ok:
                        data_set[f'{client.id}'].delete() # сообщение отправлено, удалил
                        Message.objects.filter(id=mesage_id).update(status='sent')
                except Exception as ex:
                    logging.info(repr(ex))
        if data_set:
            raise self.retry(exc='error', countdown=60 * 60)
    else:
        return f'Рассылка {mailing_id} не существует'
