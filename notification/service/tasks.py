import os
import requests

from notification.celery import app
from service.models import Mailing, Client, Message


header = {
            "Authorization": "Bearer {}".format(os.getenv("TOKEN")),
            "Content-Type": "application/json",
        }

@app.task
def send_messages(mailing_id, data_set):
    mailing = Mailing.objects.filter(id=mailing_id).first() # для проверки, что рассылка еще не удалена
    print('Выполняется')
    if mailing:
        print('mailing существует')
        if mailing.need_to_send:
            print('mailing надо отправить')
            clients = Client.objects.filter(mobile_code=mailing.mobile_code, tag=mailing.tag)
            for client in clients:
                mesage_id = data_set[client.pk]
                data = {"id": mesage_id, "phone": int(client.phone), "text": mailing.text}
                req = requests.post(url=f'https://probe.fbrq.cloud/v1/send/{mesage_id}', headers=header, json=data)
                print(req)
                print(req.json())
                Message.objects.filter(id=mesage_id).update(status='sent')
            print(f'Рассылка {mailing_id} произведена успешно')
        else:
            # попытаться отправить позже
            send_messages.delay(mailing_id, data_set)
            print(f'Рассылка {mailing_id} в ожидании')
    else:
        print(f'Рассылка {mailing_id} не существует')
