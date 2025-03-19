from rest_framework import viewsets, mixins
from .models import TaskList
from .serializers import TaskListSerializer
from .permissions import IsAllowdToEditTaskListOrNone


class TaskListViewSet(
    viewsets.GenericViewSet,
    mixins.CreateModelMixin,
    mixins.UpdateModelMixin,
    mixins.RetrieveModelMixin,
    mixins.ListModelMixin,
    mixins.DestroyModelMixin
):
    permission_classes = [IsAllowdToEditTaskListOrNone,]
    queryset = TaskList.objects.all()
    serializer_class = TaskListSerializer
