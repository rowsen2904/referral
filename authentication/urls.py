from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from .views import ActivateInviteCodeView, MyRefferalsView, UserListView

urlpatterns = [
    path('profile/activate-invite/',
         ActivateInviteCodeView.as_view(), name='activate-invite'),
    path('profiles/', UserListView.as_view(), name='user-list'),
    path('profile/my-refferals/',
         MyRefferalsView.as_view(), name='my-refferals'),
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]
