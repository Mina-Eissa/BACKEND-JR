from rest_framework import viewsets
from ..permissions import IsOwnerOrReadOnly
from rest_framework_simplejwt.authentication import JWTAuthentication
from ..models import Product
from ..serializers import ProductSerializer

class CRUDProduct(viewsets.ModelViewSet):
    serializer_class = ProductSerializer
    queryset = Product.objects.all()
    permission_classes = [IsOwnerOrReadOnly]
    authentication_classes = [JWTAuthentication]
    
