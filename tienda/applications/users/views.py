from firebase_admin import credentials, auth
import firebase_admin
from rest_framework.views import APIView
from .serializers import LoginSocialSerializer
from rest_framework.authtoken.models import Token
from rest_framework.response import Response


from django.shortcuts import render
from django.views.generic import TemplateView
from .models import User


# Create your views here.


class LoginUser(TemplateView):
    template_name = "users/login.html"


class GoogleLoginView(APIView):
    serializer_class = LoginSocialSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        print(request.data)
        serializer.is_valid(raise_exception=True)

        id_token = serializer.data.get("token_id")
        decoded_token = auth.verify_id_token(id_token)
        print("*******")
        print(decoded_token)

        name = decoded_token["name"]
        email = decoded_token["email"]
        print("=====================")
        print(name)
        print(email)

        usuario, created = User.objects.get_or_create(
            email=email, defaults={"full_name": name, "email": email, "is_active": True}
        )

        if created:
            token = Token.objects.create(user=usuario)
        else:
            token = Token.objects.get(user=usuario)
        user_get = {
            "id": usuario.pk,
            "email": usuario.email,
            "full_name": usuario.full_name,
            "date_birth": usuario.date_birth,
        }

        return Response({"token": token.key, "user_get": user_get})
