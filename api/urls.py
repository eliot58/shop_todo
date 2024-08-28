from django.urls import path
from .views import OfferView, LoginView, invoice, payment_webhook

urlpatterns = [
    path('offers/', OfferView.as_view()),
    path('login/', LoginView.as_view()),
    path('invoice/<str:code>/', invoice),
    path('webhook/', payment_webhook),
]