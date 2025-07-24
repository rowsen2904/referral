from django.utils.translation import gettext_lazy as _
from rest_framework.generics import ListAPIView
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status

from .serializers import ActivateInviteCodeSerializer, UserSerializer
from .models import User


class UserListView(ListAPIView):
    """
    For testing purposes
    """
    queryset = User.objects.all()
    serializer_class = UserSerializer


class ActivateInviteCodeView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = ActivateInviteCodeSerializer(
            data=request.data, context={"request": request})
        if serializer.is_valid():
            serializer.save()
            return Response({"message": _("Invite code successfully activated")})
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
