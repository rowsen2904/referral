from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from .views import ActivateInviteCodeView

urlpatterns = [
    path('profile/activate-invite/',
         ActivateInviteCodeView.as_view(), name='activate-invite'),
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]
