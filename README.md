# Сервис уведомлений


## Стек технологий

>Язык: __Python 3__<br>
Web фремворк: __Django & DRF__<br>
База данных: __PostgreSQL__<br>

Другое: Docker, Swagger, celery

## API Views

> - <p>/api/v1/mailing/change/int/ — обновление/удаление рассылки;<br>
> - <p>/api/v1/mailing/create/ — создание рассылки;<br>
> - <p>/api/v1/client/change/int/ — обновление/удаление клиента;<br>
> - <p>/api/v1/client/create/ — создание клиента;<br>
> - <p>/api/v1/mailing/detail/int/ — получения детальной статистики отправленных сообщений по конкретной рассылке;<br>
> - <p>/api/v1/mailing/detail_list/ — получения общей статистики по созданным рассылкам и количеству отправленных сообщений по ним с группировкой по статусам;<br>
## Swagger
> - <p>/docs/ — Swagger.<br></p>

## Приватная информация

>Скрытая информация в файле .env:<br>
>>PASSWORD — пароль от postgres;<br>
SECRET_KEY — django key;<br>
TOKEN — токен.<br>

## Запуск
1. Склонируйте репозиторий и перейдите в директорию проекта, активируйте виртуальное окружение
```
git clone https://github.com/anton431/notification_service
```
2. Установите все необходимые зависимости:
```
pip install -r requirements.txt
```
3. Выполните миграции в базу данных:
```
python manage.py makemigrations
```
```
python manage.py migrate
```
4. Создайте суперпользователя и заполните требуемые поля:
```
python manage.py createsuperuser
```
5. Создайте образ rabbitmq:
```
docker run -d -p 5672:5672 rabbitmq
```
6. Запустите celery: <br>
- для Windows
```
celery -A notification worker -l info -P gevent
```
- для Linux
```
celery -A notification worker -l info
```
7. Запустите flower, <a href=http://localhost:5566/>тут</a> вы сможете отслеживать задачи:
```
celery flower --port=5566
```
8. Запустите сервер:
```
python .\manage.py runserver 
```
