from rest_framework import serializers
from ..models import Article
from .TagSerializer import TagSerializer


class ArticleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Article
        fields = '__all__'
