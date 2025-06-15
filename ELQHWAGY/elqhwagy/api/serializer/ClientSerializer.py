from rest_framework import serializers
from ..models import Client



class ClientSerializer(serializers.ModelSerializer):
    id = serializers.CharField(read_only=True)
    last_login = serializers.DateTimeField(format="%Y-%m-%d %H:%M:%S",read_only=True)
    date_joined = serializers.DateTimeField(format="%Y-%m-%d %H:%M:%S",read_only=True)
    
    class Meta:
        model = Client
        fields = '__all__'