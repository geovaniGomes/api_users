
from django.contrib import admin
from django.urls import include, path


from permissions.api.viewsets import PermissionVieweSet
from rest_framework import routers
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from users.api.viewsets import MyObtainTokenPairView, UserVieweSet

router = routers.DefaultRouter()
router.register(r"users", UserVieweSet)
router.register(r"permissions", PermissionVieweSet)


urlpatterns = [
    path('', include(router.urls)),
    path('token/', MyObtainTokenPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('admin/', admin.site.urls),
]
