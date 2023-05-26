import os
import requests
from service.models import Mailing, Client, Message


header = {
            "Authorization": "Bearer {}".format(os.getenv("TOKEN")),
            "Content-Type": "application/json",
        }

def send_massages(mailing_id):
    mailing = Mailing.objects.filter(id=mailing_id).first() # для проверки, что рассылка еще не удалена
    if mailing:
        if mailing.need_to_send:
            clients = Client.objects.filter(mobile_code=mailing.mobile_code, tag=mailing.tag)  # если рассылку изменили и сообщения другим
            for client in clients:
                message = Message.objects.filter(mailing_id=mailing.id, client_id=client.id).first() # если рассылку изменили и сообщения другим
                data = {"id": message.pk, "phone": client.phone, "text": mailing.text}
                req = requests.post(url=f'https://probe.fbrq.cloud/v1/send/{mailing.pk}', headers=header, json=data)
                print(req.json())
