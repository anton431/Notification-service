from django.db import models
from django.utils import timezone
from django.core.exceptions import ValidationError


class Mailing(models.Model):
    launch_data = models.DateTimeField("Дата запуска рассылки")
    end_data = models.DateTimeField("Дата окончания рассылки")
    text = models.TextField("Текст", max_length=500)
    tag = models.CharField('Тег', max_length=30, blank=True)
    mobile_code = models.CharField("Код мобильного оператора", max_length=3, blank=True)

    def __str__(self):
        return str(self.pk)

    def clean(self, *args, **kwargs):
        # Не допускаем время раньше, чем сейчас и запуска.
        if self.end_data < timezone.now():
            raise ValidationError(f'Дата окончания рассылки должна быть позже, чем {timezone.now()}')
        if self.end_data < self.launch_data:
            raise ValidationError(f'Дата окончания рассылки должна быть позже, чем дата запуска')

    def total_sent(self):
        return self.messages.filter(status='sent').count()

    class Meta:
        verbose_name = "Рассылка"
        verbose_name_plural = "Рассылки"


class Client(models.Model):
    phone = models.CharField('Номер телефона', max_length=11, unique=True)
    mobile_code = models.CharField("Код мобильного оператора", max_length=3)
    tag = models.CharField("Тег", max_length=30, blank=True)
    timezone = models.CharField("Часовой пояс", max_length=40, default="UTC")

    def __str__(self):
        return self.phone

    class Meta:
        verbose_name = "Клиент"
        verbose_name_plural = "Клиенты"


class Message(models.Model):
    SENT = "sent"
    WAITING = "waiting"

    STATUS_CHOICES = [
        (SENT, "Отправлено"),
        (WAITING, "В ожидании"),
    ]
    date_creation = models.DateTimeField("Время создания", auto_now_add=True)
    status = models.CharField("Статус", choices=STATUS_CHOICES, max_length=15)
    mailing = models.ForeignKey(Mailing, on_delete=models.CASCADE,
                                related_name='messages', verbose_name='Рассылка')
    client = models.ForeignKey(Client, on_delete=models.CASCADE,
                               related_name='messages', verbose_name='Клиент')

    def __str__(self):
        return f"ID собщения {self.pk}: Cтатус {self.status}, " \
               f"номер телефона клиента {self.client}"

    class Meta:
        verbose_name = "Сообщение"
        verbose_name_plural = "Сообщения"
