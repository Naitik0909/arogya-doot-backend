import jwt
from django.conf import settings
from django.contrib.auth.models import User

from rest_framework_simplejwt.tokens import RefreshToken


def get_user(access_token):
    try:
        payload = jwt.decode(jwt=access_token, key=settings.SECRET_KEY, algorithms=['HS256'])
        print('payload 1 ' + str(payload))
        user = User.objects.get(id=payload['user_id'])
        print(user)
        return user
    except Exception as e:
        print(e)
        return False

# Get Tokens Manually
# def get_tokens_for_user(user):
#     refresh = RefreshToken.for_user(user)
#     user_type = None
#     if JobSeeker.objects.filter(user = user).exists():
#         user_type = 'JobSeeker'
#     elif DistrictAdmin.objects.filter(user=user).exists() or DistrictNonAdmin.objects.filter(user=user).exists():
#         user_type = 'DistrictAdmin'
#     return {
#         'refresh': str(refresh),
#         'access': str(refresh.access_token),
#         'user' : user_type
#     }
