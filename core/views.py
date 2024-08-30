from django.shortcuts import render
from api.models import Offer
from api.jwt_utils import decode_access_token

def login_view(request):
    return render(request, 'login.html')


def index(request):
    token =  request.COOKIES.get('token')
    if token:
        payload = decode_access_token(token)
        offers = Offer.objects.filter(params__sellerCode=payload["sub"])
    else:
        offers = []
    return render(request, 'index.html', {"offers": offers})

