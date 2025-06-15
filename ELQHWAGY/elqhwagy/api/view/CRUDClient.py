from rest_framework import viewsets
from ..permissions import IsOwnerOrReadOnly
from rest_framework_simplejwt.authentication import JWTAuthentication
from ..models import Client
from ..serializers import ClientSerializer

class CRUDClient(viewsets.ModelViewSet):
    serializer_class = ClientSerializer
    queryset = Client.objects.all()
    permission_classes = [IsOwnerOrReadOnly]
    authentication_classes = [JWTAuthentication]
    
