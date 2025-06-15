from rest_framework import serializers
from ..models import Task
from .TagSerializer import TagSerializer

class TaskStatusUpdateSerializer(serializers.ModelSerializer):
    tags = serializers.ListField(
        child=serializers.CharField(), write_only=True,required=False
    )
    tag_objects = TagSerializer(many=True, read_only=True, source='tags')
    status = serializers.ChoiceField(Task.TaskStatus)
    class Meta:
        model = Task
        fields = '__all__'
        read_only_fields = [ field.name for field in model._meta.fields if field.name != 'status']
