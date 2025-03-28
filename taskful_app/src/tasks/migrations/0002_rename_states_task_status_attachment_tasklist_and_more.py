# Generated by Django 5.1.7 on 2025-03-19 03:25

import django.db.models.deletion
import tasks.models
import uuid
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        (
            "houses",
            "0002_rename_not_completed_task_count_house_not_completed_tasks_count",
        ),
        ("tasks", "0001_initial"),
        ("users", "0002_profile_house"),
    ]

    operations = [
        migrations.RenameField(
            model_name="task",
            old_name="states",
            new_name="status",
        ),
        migrations.CreateModel(
            name="Attachment",
            fields=[
                (
                    "id",
                    models.UUIDField(
                        default=uuid.uuid4,
                        editable=False,
                        primary_key=True,
                        serialize=False,
                    ),
                ),
                (
                    "data",
                    models.FileField(
                        upload_to=tasks.models.GenerateAttachmentFilePath()
                    ),
                ),
                (
                    "task",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="attachments",
                        to="tasks.task",
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="TaskList",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("created_on", models.DateTimeField(auto_now_add=True)),
                ("completed_on", models.DateTimeField(blank=True, null=True)),
                ("name", models.CharField(max_length=120)),
                ("description", models.TextField(blank=True, null=True)),
                (
                    "status",
                    models.CharField(
                        choices=[("NC", "Not Completed"), ("C", "Completed")],
                        default="NC",
                        max_length=2,
                    ),
                ),
                (
                    "created_by",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        related_name="lists",
                        to="users.profile",
                    ),
                ),
                (
                    "house",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="lists",
                        to="houses.house",
                    ),
                ),
            ],
        ),
        migrations.AddField(
            model_name="task",
            name="task_list",
            field=models.ForeignKey(
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                related_name="tasks",
                to="tasks.tasklist",
            ),
        ),
    ]
