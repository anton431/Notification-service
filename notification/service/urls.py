from django.urls import path

from service.views import MailingDetailAPIView, \
    MailingCreateAPIView, ClientDetailAPIView, \
    ClientCreateAPIView, MailingRetrieveAPIView, MailingListAPIView

urlpatterns = [
    path('api/v1/mailing/change/<int:pk>/',
         MailingDetailAPIView.as_view()),
    path('api/v1/mailing/create/', MailingCreateAPIView.as_view()),
    path('api/v1/client/change/<int:pk>/',
         ClientDetailAPIView.as_view()),
    path('api/v1/client/create/', ClientCreateAPIView.as_view()),
    path('api/v1/mailing/detail/<int:pk>/',
         MailingRetrieveAPIView.as_view()),
    path('api/v1/mailing/detail_list/', MailingListAPIView.as_view()),
]
