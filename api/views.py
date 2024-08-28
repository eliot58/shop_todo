import json
import requests
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Offer
from .serializers import OfferSerializer, LoginSerializer

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
            return Response(data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
