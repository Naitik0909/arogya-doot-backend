from django.urls import path

from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

from .views import RegisterUser, BlacklistToken, LoginUser

urlpatterns = [
    path('register/', RegisterUser.as_view(),name="register"),
    path('login/', LoginUser.as_view(), name="login"),
    path('logout/blacklist/', BlacklistToken.as_view(),name="blacklist"),
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]