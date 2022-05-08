from django.contrib import admin
from django.urls import path, include

from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi

schema_view = get_schema_view(
   openapi.Info(
      title="Arogya Doot APIs",
      default_version='v1',
      description="Request and Response sets for all the APIs",
      terms_of_service="https://www.google.com/policies/terms/",
      contact=openapi.Contact(email="parmarnaitik0909@gmail.com"),
      license=openapi.License(name="No License"),
   ),
   public=True,
   permission_classes=(permissions.AllowAny,),
)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('auth/', include('users.urls')),
    path('patient/', include('patient.urls')),
    path('doctor/', include('doctor.urls')),
    path('nurse/', include('nurse.urls')),
    path('schema/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
]
