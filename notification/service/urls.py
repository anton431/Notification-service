from django.urls import path

from service.views import MailingDetailAPIView, MailingCreateAPIView, ClientDetailAPIView, ClientCreateAPIView, \
    MailingRetrieveAPIView, MailingListAPIView

urlpatterns = [
    path('api/v1/mailing/change/<int:pk>/', MailingDetailAPIView.as_view()),  # обновление/удаление рассылки
    path('api/v1/mailing/create/', MailingCreateAPIView.as_view()),  # создание рассылки
    path('api/v1/client/change/<int:pk>/', ClientDetailAPIView.as_view()),  # обновление/удаление клиента
    path('api/v1/client/create/', ClientCreateAPIView.as_view()),  # создание клиента
    # получения детальной статистики отправленных сообщений по конкретной рассылке
    path('api/v1/mailing/detail/<int:pk>/', MailingRetrieveAPIView.as_view()),
    # получения общей статистики по созданным рассылкам и количеству отправленных сообщений по ним с группировкой по статусам
    path('api/v1/mailing/detail_list/', MailingListAPIView.as_view()),
]
