
from rest_framework import serializers
from ..models import Author
from .ArticleSerializer import ArticleSerializer
from django.contrib.auth.hashers import make_password


class AuthorSerializer(serializers.ModelSerializer):
    articles = ArticleSerializer(many=True, read_only=True)
    authPassword = serializers.CharField(write_only=True)

    class Meta:
        model = Author
        fields = [
            'id',
            'authName',
            'authEmail',
            'authImg',
            'authWallpaper',
            'authBirthDate',
            'authBio',
            'authCreatedAt',
            'authUpdatedAt',
            'authPassword',
            'articles'
        ]
        read_only_fields = ['id', 'authCreatedAt', 'authUpdatedAt']
        extra_kwargs = {
            'authEmail': {'required': True},
            'authName': {'required': True}
        }

    def create(self, validated_data):
        password = validated_data.pop('authPassword')
        password = make_password(password)
        validated_data['authPassword'] = password
        author = Author(**validated_data)
        author.set_password(password)
        author.save()
        return author

    def update(self, instance, validated_data):
        password = validated_data.pop('authPassword')
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        if password:
            password = make_password(password)
            validated_data['authPassword'] = password
            instance.set_password(password)
        instance.save()
        return instance
