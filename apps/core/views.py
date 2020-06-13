from django.contrib.auth import login as auth_login
from django.contrib.auth import logout as auth_logout
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import ensure_csrf_cookie
from rest_framework import response
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView

from .models import User


@method_decorator(ensure_csrf_cookie, name="dispatch")
class LoginView(APIView):
    def post(self, request, *args, **kwargs):
        user = User.objects.filter(username=request.data["username"]).first()

        if user and user.check_password(request.data["password"]):
            auth_login(request, user)
            return response.Response()

        return response.Response(status=401)


@method_decorator(ensure_csrf_cookie, name="dispatch")
class MeView(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request, *args, **kwargs):
        return response.Response()


@method_decorator(ensure_csrf_cookie, name="dispatch")
class LogoutView(APIView):
    permission_classes = (IsAuthenticated,)

    def delete(self, request, *args, **kwargs):
        auth_logout(request)
        return response.Response()
