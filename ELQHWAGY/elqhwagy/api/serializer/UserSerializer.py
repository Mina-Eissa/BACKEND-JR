from rest_framework import serializers
from ..models import User
from django.contrib.auth.hashers import make_password

class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only = True)
    last_login = serializers.DateTimeField(format="%Y-%m-%d %H:%M:%S",read_only=True)
    date_joined = serializers.DateTimeField(format="%Y-%m-%d %H:%M:%S",read_only=True)
    class Meta:
        model = User
        # fields = '__all__'
        exclude = ['user_permissions','groups']

    def create(self, validated_data):
        # Hash the password before saving
        validated_data['password'] = make_password(validated_data['password'])
        return super().create(validated_data)
    
    def update(self,instance,validated_data):
        password = validated_data.pop('password', None)
        if password:
            instance.password = make_password(password)
        return super().update(instance, validated_data)

