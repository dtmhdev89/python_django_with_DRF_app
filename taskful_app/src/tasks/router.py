from rest_framework import routers
from .viewsets import TaskListViewSet


app_name = "tasks"
router = routers.DefaultRouter()
router.register("tasklists", TaskListViewSet)
