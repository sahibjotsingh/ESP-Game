from django.contrib import admin
from django.urls import path
from api.views import *
from django.conf.urls import url, include

from rest_framework.routers import DefaultRouter
from django.conf import settings
from django.conf.urls.static import static
from rest_framework_extensions.routers import NestedRouterMixin
from rest_framework.authtoken.views import obtain_auth_token  # <-- Here

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api-token-auth/', obtain_auth_token, name='api_token_auth'),  # <-- And here
]

class NestedDefaultRouter(NestedRouterMixin, DefaultRouter):
    pass

router = NestedDefaultRouter()
primary_image_router = router.register('primary-images', PrimaryImageViewSet, basename='primary_image') 
router.register('secondary-images', SecondaryImageViewSet, basename='secondary_image_1') 
primary_image_router.register('secondary-image', SecondaryImageViewSet, basename='secondary_image', parents_query_lookups=['related_image'])

router.register('tasks', TaskViewSet, basename='tasks') 

router.register('myuser', MyUserViewSet, basename='myuser')

router.register('user', UserViewSet, basename='user')

urlpatterns += router.urls

if settings.DEBUG:
	urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)



