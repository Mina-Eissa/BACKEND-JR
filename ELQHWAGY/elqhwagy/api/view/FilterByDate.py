from rest_framework.decorators import api_view,authentication_classes,permission_classes
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from ..permissions import IsOwnerOrReadOnly
from rest_framework_simplejwt.authentication import JWTAuthentication	
from ..models import Client,Order,Product,User
from ..serializers import ClientSerializer
from datetime import datetime

@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
def FilterClientByDate(request,start,end):
    """
    Filter clients by date range.
    """
    if request.method == 'GET':
        try:
            date_start = datetime.strptime(start, "%Y-%m-%d").date()
            date_end = datetime.strptime(end, "%Y-%m-%d").date()
            clients = Client.objects.filter(created_at__range=[date_start, date_end])
            serializer = ClientSerializer(clients, many=True)
            return Response(serializer.data)
        except ValueError:
            return Response({"error": "Invalid date format. Use YYYY-MM-DD."}, status=status.HTTP_400_BAD_REQUEST)
    else:
        return Response({"detail": "Method not allowed"}, status=status.HTTP_405_METHOD_NOT_ALLOWED)
