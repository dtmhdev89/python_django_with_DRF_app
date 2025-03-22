from rest_framework import serializers
from .models import Task, TaskList, Attachment
from houses.models import House


class TaskListSerializer(serializers.ModelSerializer):
    house = serializers.HyperlinkedRelatedField(
        queryset=House.objects.all(),
        many=False,
        view_name="house-detail"
    )
    created_by = serializers.HyperlinkedRelatedField(
        read_only=True,
        many=False,
        view_name="profile-detail"
    )
    tasks = serializers.HyperlinkedRelatedField(
        read_only=True,
        many=True,
        view_name="task-detail"
    )
    
    class Meta:
        model = TaskList
        fields = [
            "url", "id", "name", "description", "status",
            "created_on", "created_by", "house", "tasks"
        ]
        read_only_fields = ["created_on", "status"]


class TaskSerializer(serializers.ModelSerializer):

    created_by = serializers.HyperlinkedRelatedField(
        read_only=True,
        many=False,
        view_name="profile-detail"
    )
    completed_by = serializers.HyperlinkedRelatedField(
        read_only=True,
        many=False,
        view_name="profile-detail"
    )
    task_list = serializers.HyperlinkedRelatedField(
        queryset=TaskList.objects.all(),
        many=False,
        view_name="tasklist-detail"
    )
    attachments = serializers.HyperlinkedRelatedField(
        read_only=True,
        many=True,
        view_name="attachment-detail"
    )

    class Meta:
        model = Task
        fields = [
            "url", "id", "name", "description", "status",
            "created_on", "completed_on", "created_by", "completed_by",
            "task_list", "attachments"
        ]
        read_only_fields = [
            "created_on", "completed_on", "created_by",
            "completed_by", "status"
        ]

    def validate_task_list(self, value):
        user_profile = self.context['request'].user.profile
        user_task_lists = user_profile.house.lists
        if value not in user_task_lists.all():
            raise serializers.ValidationError(
                "TaskList provided does not belong to house for which user is a member"
            )
        
        return value

    def create(self, validated_data):
        current_user_profile = self.context["request"].user.profile
        task = Task.objects.create(**validated_data)
        task.created_by = current_user_profile
        task.save()

        return task

class AttachmentSerializer(serializers.ModelSerializer):
    task = serializers.HyperlinkedRelatedField(
        queryset=Task.objects.all(),
        many=False,
        view_name="task-detail"
    )

    class Meta:
        model = Attachment
        fields = [
            "url", "id", "created_on", "data", "task"
        ]
        read_only_fields = ["created_on"]

    def validate(self, attrs):
        current_user_profile = self.context["request"].user.profile
        task = attrs["task"]
        task_list = TaskList.objects.get(tasks__id__exact=task.id)
        if task_list not in current_user_profile.house.lists.all():
            raise serializers.ValidationError(
                {"task": "Task provided does not belong to house for which user is a member"}
            )
        
        return attrs
