from django.urls import path

from service.views import MailingDetailAPIView, MailingCreateAPIView, ClientDetailAPIView, ClientCreateAPIView

urlpatterns = [
    path('api/v1/mailing/<int:pk>/', MailingDetailAPIView.as_view()),
    path('api/v1/mailing/create/', MailingCreateAPIView.as_view()),
    path('api/v1/client/<int:pk>/', ClientDetailAPIView.as_view()),
    path('api/v1/client/create/', ClientCreateAPIView.as_view()),
]