
from django.contrib import admin
from django.urls import include, path


from core.api.permissions.viewsets import PermissionViewSet
from core.api.groups.viewsets import GroupViewSet
from rest_framework import routers
from rest_framework_simplejwt.views import TokenRefreshView
from core.api.users.viewsets import ObtainMyTokenView, UserViewSet


router = routers.DefaultRouter()
router.register(r"users", UserViewSet)
router.register(r"permissions", PermissionViewSet)
router.register(r"groups", GroupViewSet)


urlpatterns = [
    path('', include(router.urls)),
    path('auth/', ObtainMyTokenView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('admin/', admin.site.urls),
]
