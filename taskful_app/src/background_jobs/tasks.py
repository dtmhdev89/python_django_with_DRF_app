from background_task import background
from background_task.tasks import Task as BT

from houses.models import House
from tasks.models import COMPLETE


@background(schedule=10)
def calculate_house_status():
    for house in House.objects.all():
        total_tasks = 0
        completed_tasks_count = 0
        house_task_lists = house.lists.all()
        for task_list in house_task_lists:
            total_tasks += task_list.tasks.count()
            completed_tasks_count += task_list.tasks.filter(status=COMPLETE).count()
        
        house.completed_tasks_count = completed_tasks_count
        house.not_completed_tasks_count = total_tasks - completed_tasks_count
        house.save()

if not BT.objects.filter(verbose_name="calculate_house_status").exists():
    calculate_house_status(
        repeat=BT.DAILY,
        verbose_name="calculate_house_status",
        priority=0
    )
