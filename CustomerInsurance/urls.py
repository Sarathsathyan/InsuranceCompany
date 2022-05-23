from django.urls import path, include
from rest_framework import routers
from rest_framework_simplejwt import views as jwt_views
router = routers.SimpleRouter()
from .views import PolicyViewSet, ProgressViewSet


router.register(r'policy', PolicyViewSet)
router.register(r'statistics', ProgressViewSet)
urlpatterns = [
    path('', include(router.urls)),

    path('token-auth/', jwt_views.TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token-refresh/', jwt_views.TokenRefreshView.as_view(), name='token_refresh'),

]