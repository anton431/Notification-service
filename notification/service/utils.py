import os
import requests
from service.models import Mailing, Client, Message


header = {
            "Authorization": "Bearer {}".format(os.getenv("TOKEN")),
            "Content-Type": "application/json",
        }

def send_messages(mailing_id, data_set):
    mailing = Mailing.objects.filter(id=mailing_id).first() # для проверки, что рассылка еще не удалена
    print('Выполняется')
    if mailing:
        print('mailing существует')
        if mailing.need_to_send:
            print('mailing надо отправить')
            for client in data_set['clients']:
                mesage_id = data_set['client_set'][client.pk]
                data = {"id": mesage_id, "phone": int(client.phone), "text": mailing.text}
                print(data)
                req = requests.post(url=f'https://probe.fbrq.cloud/v1/send/{mesage_id}', headers=header, json=data)
                print(req)
                print(req.json())
                Message.objects.filter(id=mesage_id).update(status='sent')
                print(mesage_id)
            print(f'Рассылка {mailing_id} произведена успешно')
        else:
            # попытаться отправить позже
            print(f'Рассылка {mailing_id} в ожидании')
    else:
        print(f'Рассылка {mailing_id} была удалена')
