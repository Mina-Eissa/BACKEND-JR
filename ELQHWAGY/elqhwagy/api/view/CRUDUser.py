from rest_framework import viewsets,status
from rest_framework.response import Response
from ..permissions import IsOwnerOrReadOnly
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework_simplejwt.tokens import RefreshToken
from ..serializers import UserSerializer
from ..models import User

class CRUDUser(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthentication]
    serializer_class= UserSerializer
    queryset = User.objects.all()

    def create(self, request, *args, **kwargs):
        if not request.user.is_superuser:
            return Response({'detail': 'Only superusers can create users.'}, status=status.HTTP_403_FORBIDDEN)
        
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        user = serializer.instance
        refresh = RefreshToken.for_user(user = user )
        headers = self.get_success_headers(serializer.data)
        return Response({
            'user': serializer.data,
            'refresh': str(refresh),
            'access': str(refresh.access_token)
        }, status=status.HTTP_201_CREATED, headers=headers)
    
    def update(self, request, *args, **kwargs):
        if not request.user.is_superuser:
            return Response({'detail': 'Only superusers can update users.'}, status=status.HTTP_403_FORBIDDEN)

        return super().update(request, *args, **kwargs)
