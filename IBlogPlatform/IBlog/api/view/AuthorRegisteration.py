from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny
from rest_framework_simplejwt.tokens import RefreshToken
from ..models import Author
from ..serializers import AuthorSerializer


class AuthorRegistrationView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = AuthorSerializer(data=request.data)
        if serializer.is_valid():
            author = serializer.save()
            refresh = RefreshToken.for_user(author)
            return Response({
                'refresh': str(refresh),
                'access': str(refresh.access_token),
                'author': serializer.data
            }, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
