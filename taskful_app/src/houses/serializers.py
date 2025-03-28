from rest_framework import serializers
from .models import House


class HouseSerializer(serializers.ModelSerializer):

    members_count = serializers.IntegerField(read_only=True)
    members = serializers.HyperlinkedRelatedField(
        read_only=True,
        many=True,
        view_name="profile-detail"
    )
    manager = serializers.HyperlinkedRelatedField(
        read_only=True,
        many=False,
        view_name="profile-detail"
    )
    task_lists = serializers.HyperlinkedRelatedField(
        read_only=True,
        many=True,
        view_name="tasklist-detail",
        source="lists" # lists is a related name as a relationship between House and TaskList model in tasks app
    )

    class Meta:
        model = House
        fields = [
            'url', 'id', 'image', 'name', 'created_on',
            'manager', 'description', 'members_count', 'points',
            'completed_tasks_count', 'not_completed_tasks_count',
            'members', "task_lists"
        ]
        read_only_fields = [
            "points",
            'compeleted_tasks_count',
            'not_completed_tasks_count'
        ]
