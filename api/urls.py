from django.urls import path
from .views import OfferView, LoginView

urlpatterns = [
    path('offers/', OfferView.as_view()),
    path('login/', LoginView.as_view()),
]