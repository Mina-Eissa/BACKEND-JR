from rest_framework import serializers
from ..models import Task, Tag
from .TagSerializer import TagSerializer
from django.utils import timezone
from dateutil.relativedelta import relativedelta
from datetime import timedelta

class TaskSerializer(serializers.ModelSerializer):
    tags = serializers.ListField(
        child=serializers.CharField(), write_only=True,required=False
    )
    remain_time = serializers.SerializerMethodField(read_only=True)
    tag_objects = TagSerializer(many=True, read_only=True, source='tags')
    def get_remain_time(self, obj):
        now = timezone.now()

        if obj.deadline <= now:
            return {
                "years": 0,
                "months": 0,
                "days": 0,
                "hours": 0,
                "minutes": 0,
                "seconds": 0
            }

        delta = relativedelta(obj.deadline, now)

        return {
            "years": delta.years,
            "months": delta.months,
            "days": delta.days,
            "hours": delta.hours,
            "minutes": delta.minutes,
            "seconds": delta.seconds
        }

    class Meta:
        model = Task
        fields = '__all__'

    def create(self, validated_data):
        tag_names = validated_data.pop('tags', [])
        task = Task.objects.create(**validated_data)

        tag_instances = []
        for name in tag_names:
            tag, created = Tag.objects.get_or_create(name=name)
            tag_instances.append(tag)
        task.tags.set(tag_instances)

        return task

    def update(self, instance, validated_data):
        tag_names = validated_data.pop('tags', None)
        if tag_names is not None:
            tag_instances = [Tag.objects.get_or_create(
                name=name)[0] for name in tag_names]
            instance.tags.set(tag_instances)

        return super().update(instance, validated_data)
