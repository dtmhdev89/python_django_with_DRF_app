from rest_framework import viewsets, mixins, status, filters
from rest_framework.decorators import action
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from django.utils import timezone
from .models import TaskList, Task, Attachment
from .models import COMPLETE, NOT_COMPLETE
from .serializers import TaskListSerializer, TaskSerializer, AttachmentSerializer
from .permissions import IsAllowdToEditTaskListOrNone, IsAllowedToEditTaskElseNone, \
    IsAllowdToEditAttachmentElseNone


class TaskStatusException(Exception):
    pass


class TaskListViewSet(
    viewsets.GenericViewSet,
    mixins.CreateModelMixin,
    mixins.UpdateModelMixin,
    mixins.RetrieveModelMixin,
    mixins.DestroyModelMixin
):
    permission_classes = [IsAllowdToEditTaskListOrNone,]
    queryset = TaskList.objects.all()
    serializer_class = TaskListSerializer


class TaskViewSet(
    viewsets.ModelViewSet
):
    permission_classes = [IsAllowedToEditTaskElseNone]
    queryset = Task.objects.all()
    serializer_class = TaskSerializer
    filter_backends = [filters.SearchFilter, DjangoFilterBackend]
    search_fields = ["name", "description"]
    filterset_fields = ["status"]

    def get_queryset(self):
        queryset =  super().get_queryset()
        current_user_profile = self.request.user.profile
        updated_queryset = queryset.filter(created_by=current_user_profile)

        return updated_queryset

    @action(detail=True, methods=["PATCH"])
    def update_task_status(self, request, pk=None):
        try:
            task = self.get_object()
            profile = request.user.profile
            input_status = request.data["status"]
            if input_status == NOT_COMPLETE:
                if task.status == NOT_COMPLETE:
                    raise TaskStatusException("Task is already marked as not complete")
                
                task.status = NOT_COMPLETE
                task.completed_on = None
                task.completed_by = None
            elif input_status == COMPLETE:
                if task.status == COMPLETE:
                    raise TaskStatusException("Task is already marked as complete")
                
                task.status = COMPLETE
                task.completed_on = timezone.now()
                task.complted_by = profile
            else:
                raise TaskStatusException("Incorrect status provided")
            
            task.save()
            serializer = TaskSerializer(instance=task, context={"request": request})
            return Response(serializer.data, status=status.HTTP_200_OK)
        except TaskStatusException as e:
            return Response({"detail": str(e)}, status=status.HTTP_400_BAD_REQUEST)


class AttachmentViewSet(
    viewsets.GenericViewSet,
    mixins.CreateModelMixin,
    mixins.UpdateModelMixin,
    mixins.RetrieveModelMixin,
    mixins.DestroyModelMixin
):
    permission_classes = [IsAllowdToEditAttachmentElseNone]
    queryset = Attachment.objects.all()
    serializer_class = AttachmentSerializer
