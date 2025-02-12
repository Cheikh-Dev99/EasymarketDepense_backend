from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import DepenseViewSet

router = DefaultRouter()
router.register(r'depenses', DepenseViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
