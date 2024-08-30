from django.urls import path
from .views import OfferView, LoginView, invoice, payment_webhook, add_offer

urlpatterns = [
    path('offers/', OfferView.as_view()),
    path('login/', LoginView.as_view()),
    path('invoice/<str:code>/', invoice),
    path('webhook/', payment_webhook),
    path('add_offer/', add_offer),
]