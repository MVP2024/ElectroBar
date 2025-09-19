from django.urls import include, path
from django.contrib import admin
from rest_framework.routers import DefaultRouter

from network.views import NetworkNodeViewSet

router = DefaultRouter()
router.register(r"nodes", NetworkNodeViewSet, basename="networknode")

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", include(router.urls)),
]
