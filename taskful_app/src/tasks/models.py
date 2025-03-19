import os
from django.utils.deconstruct import deconstructible
from django.db import models
import uuid


# Create your models here.
NOT_COMPLETE = "NC"
COMPLETE = "C"
TASK_STATUS_CHOICES = [
    (NOT_COMPLETE, 'Not Completed'),
    (COMPLETE, 'Completed')
]


@deconstructible
class GenerateAttachmentFilePath(object):
    def __init__(self):
        pass

    def __call__(self, instance, filename):
        ext = filename.split(".")[-1]
        path = f"tasks/{instance.id}/attachments"
        name = f"{instance.id}.{ext}"

        return os.path.join(path, name)


attachment_file_path = GenerateAttachmentFilePath()


class Attachment(models.Model):
    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False
    )
    data = models.FileField(upload_to=attachment_file_path)
    task = models.ForeignKey(
        "tasks.Task",
        on_delete=models.CASCADE,
        related_name="attachments"
    )
    created_on = models.DateTimeField(auto_now_add=True, null=True)

    def __str__(self):
        return f"{self.id} | {self.task}"


class TaskList(models.Model):
    created_on = models.DateTimeField(auto_now_add=True)
    completed_on = models.DateTimeField(null=True, blank=True)
    house = models.ForeignKey(
        "houses.House",
        on_delete=models.CASCADE,
        related_name="lists"
    )
    created_by = models.ForeignKey(
        "users.Profile",
        blank=True,
        null=True,
        on_delete=models.SET_NULL,
        related_name="lists"
    )
    name = models.CharField(max_length=120)
    description = models.TextField(null=True, blank=True)
    status = models.CharField(
        max_length=2,
        choices=TASK_STATUS_CHOICES,
        default=NOT_COMPLETE
    )

    def __str__(self) -> str:
        return f"{self.id} | {self.name}"


class Task(models.Model):
    created_on = models.DateTimeField(auto_now_add=True)
    completed_on = models.DateTimeField(null=True, blank=True)
    created_by = models.ForeignKey(
        "users.Profile",
        blank=True,
        null=True,
        on_delete=models.SET_NULL,
        related_name="created_tasks"
    )
    completed_by = models.ForeignKey(
        "users.Profile",
        blank=True,
        null=True,
        on_delete=models.SET_NULL,
        related_name="completed_tasks"
    )
    name = models.CharField(max_length=120)
    description = models.TextField(null=True, blank=True)
    status = models.CharField(
        max_length=2,
        choices=TASK_STATUS_CHOICES,
        default=NOT_COMPLETE
    )
    task_list = models.ForeignKey(
        "tasks.TaskList",
        on_delete=models.CASCADE,
        related_name="tasks",
        null=True
    )

    def __str__(self) -> str:
        return f"{self.id} | {self.name}"
