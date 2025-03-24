from django.apps import AppConfig
from django.db.models.signals import post_migrate
from django.db import connections
from django.db.utils import OperationalError


class BackgroundJobsConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "background_jobs"

    def ready(self):
        def import_tasks(sender, **kwargs):
            try:
                if "default" in connections and \
                        connections["default"].introspection.table_names():
                    import background_jobs.tasks
            except OperationalError:
                pass

        post_migrate.connect(import_tasks, sender=self)
