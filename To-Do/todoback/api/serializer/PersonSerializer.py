from rest_framework import serializers
from ..models import Person
from django.contrib.auth.password_validation import validate_password

class PersonSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=True)
    age = serializers.ReadOnlyField()
    personnal_img = serializers.ImageField(required=False, allow_null=True)

    class Meta:
        model = Person
        fields = [
            'id', 'username', 'email', 'password',
            'personnal_img', 'wallpaper_img',
            'created_at', 'updated_at', 'birth_date', 'age'
        ]

    def create(self, validated_data):
        user = Person.objects.create_user(
            username=validated_data['username'],
            email=validated_data['email'],
            password=validated_data['password'],
            birth_date=validated_data.get('birth_date'),
            personnal_img=validated_data.get('personnal_img'),
            wallpaper_img=validated_data.get('wallpaper_img'),
        )
        return user

    def to_representation(self, instance):
        data = super().to_representation(instance)
        request = self.context.get('request')

        if instance.personnal_img and request:
            data['personnal_img'] = request.build_absolute_uri(
                instance.personnal_img.url)
        else:
            data['personnal_img'] = None

        return data
