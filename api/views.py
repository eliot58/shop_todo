import json
from django.shortcuts import get_object_or_404
import requests
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from .jwt_utils import create_access_token
from .models import Offer, Order
from .serializers import OfferSerializer, LoginSerializer
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse, HttpResponseForbidden
from django.conf import settings
import uuid
from yookassa import Configuration, Payment
from django.conf import settings

class OfferView(APIView):
    def get(self, request):
        offers = Offer.objects.all()
        serializer = OfferSerializer(offers, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = OfferSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

class LoginView(APIView):

    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        if serializer.is_valid():
            username = serializer.validated_data["username"].replace("+", "%252B")
            password = serializer.validated_data["password"].replace("+", "%252B")
            r = requests.get(f'http://176.62.187.250/auth.php?jsoncallback=jQuery1113007469605505475574_1676738570680&login={username}&passwd={password}')
            s = r.text
            start = s.index('(')
            end = s.rindex(')')
            json_string = s[start+1:end]

            data = json.loads(json_string)

            if data['seller_code'] == 'empty' or data['seller_name'] == 'empty':
                return Response("Invalid login or password", status=status.HTTP_403_FORBIDDEN)
            return Response({"access_token": create_access_token(data['seller_code'])}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@csrf_exempt
def invoice(request, id):
    if request.method == "POST":
        Configuration.account_id = settings.YOOKASSA_SHOP_ID
        Configuration.secret_key = settings.YOOKASSA_SECRET_KEY

        base_url = "https://shop.todotodo.ru"

        offer = Offer.objects.get(id=id)

        payment_response = Payment.create({
            "amount": {
                "value": str(offer.params["summa"]),
                "currency": "RUB"
            },
            "confirmation": {
                "type": "redirect",
                "return_url": base_url
            },
            "capture": True,
            "description": f"Оплата заказа {offer.params['name']}",
        }, uuid.uuid4())
        order = Order.objects.create(payment_id=payment_response.id)
        offer.order = order
        offer.save()
        return JsonResponse({"confirmation_url": payment_response.confirmation.confirmation_url})

    return JsonResponse({'status': 'invalid method'}, status=405)


@csrf_exempt
def add_offer(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        offer = Offer.objects.filter(params__name=data["name"])
        if offer:
            return JsonResponse({'status': 'Bad request'}, status=400)
        t = 1 if data["name"].strip().split("\\")[0] == 'О' else 2
        order_id = data["name"].strip().split('\\')[1]

        url = f"http://176.62.187.250/offer.php?order_id={order_id}&type={t}"

        try:
            response = requests.get(url)
            if not response.status_code == 200:
                return JsonResponse({'status': 'failed'}, status=400)
        except requests.exceptions.RequestException as e:
            return JsonResponse({'status': 'failed'}, status=400)
        return JsonResponse({'status': 'success'})
    return JsonResponse({'status': 'invalid method'}, status=405)


@csrf_exempt
def payment_webhook(request):
    if request.method == 'POST':
        event_json = json.loads(request.body)
        if 'event' in event_json and event_json['event'] == 'payment.succeeded':
            payment_id = event_json['object']['id']
            order = get_object_or_404(Order, payment_id=payment_id)
            if order.paid != False:
                return HttpResponseForbidden()
            
            order.paid = True
            order.save()
            return JsonResponse({'status': 'success'})
        return JsonResponse({'status': 'failed'})
    return JsonResponse({'status': 'invalid method'}, status=405)