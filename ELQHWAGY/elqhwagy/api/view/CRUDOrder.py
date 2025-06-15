from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import ModelViewSet
from rest_framework_simplejwt.authentication import JWTAuthentication
from ..serializers import OrderSerializer
from ..models import Order
from rest_framework.response import Response
class CRUDOrder(ModelViewSet):
    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthentication]
    serializer_class = OrderSerializer
    queryset = Order.objects.all()

    
