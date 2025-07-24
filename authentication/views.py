from django.utils.translation import gettext_lazy as _
from rest_framework.generics import ListAPIView
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken

from .serializers import (
    ActivateInviteCodeSerializer,
    RequestCodeSerializer,
    UserSerializer,
    VerifyCodeSerializer,
    MyProfileSerializer,
)
from .models import User


class UserListView(ListAPIView):
    """
    For testing purposes
    """
    queryset = User.objects.all()
    serializer_class = UserSerializer


class MyProfileView(APIView):
    permission_classes = [IsAuthenticated]

    def get_serializer_class(self):
        return MyProfileSerializer

    def get(self, request):
        serializer = MyProfileSerializer(request.user)
        return Response(serializer.data)


class ActivateInviteCodeView(APIView):
    permission_classes = [IsAuthenticated]

    def get_serializer_class(self):
        return ActivateInviteCodeSerializer

    def post(self, request):
        serializer = ActivateInviteCodeSerializer(
            data=request.data, context={"request": request})
        if serializer.is_valid():
            serializer.save()
            return Response({"message": _("Invite code successfully activated")})
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class MyRefferalsView(APIView):
    permission_classes = [IsAuthenticated]

    def get_serializer_class(self):
        return UserSerializer

    def get(self, request):
        user = request.user
        refferals = user.get_referred_users()
        serializer = UserSerializer(refferals, many=True)
        return Response(serializer.data)


class RequestCodeView(APIView):
    def get_serializer_class(self):
        return RequestCodeSerializer

    def post(self, request):
        serializer = RequestCodeSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"message": _("Code sent")}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class VerifyCodeView(APIView):
    def get_serializer_class(self):
        return VerifyCodeSerializer

    def post(self, request):
        serializer = VerifyCodeSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            refresh = RefreshToken.for_user(user)
            return Response({
                "access": str(refresh.access_token),
                "refresh": str(refresh),
            })
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
