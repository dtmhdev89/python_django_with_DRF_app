from rest_framework import routers
from .viewsets import HouseViewSet

app_name = "houses"

router = routers.DefaultRouter()

router.register("houses", HouseViewSet)
