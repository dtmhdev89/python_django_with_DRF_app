# Generated by Django 5.1.7 on 2025-03-19 03:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("tasks", "0002_rename_states_task_status_attachment_tasklist_and_more"),
    ]

    operations = [
        migrations.AddField(
            model_name="attachment",
            name="created_on",
            field=models.DateTimeField(auto_now_add=True, null=True),
        ),
    ]
