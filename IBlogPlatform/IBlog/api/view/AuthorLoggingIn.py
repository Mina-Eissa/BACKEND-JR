from rest_framework import status
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken
# from ..serializers import AuthorLoggingInSerializer
from ..models import Author
from django.contrib.auth.hashers import check_password
from django.contrib.auth import get_user_model


class AuthorLoggingInView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        # serializer = AuthorLoggingInSerializer(data=request.data)
        data = request.data
        if data:
            if data.get('authName'):
                username_or_email = data['authName']
            elif data.get('authEmail'):
                username_or_email = data['authEmail']
            else:
                return Response({"error": "Username or email is required"}, status=status.HTTP_400_BAD_REQUEST)
            if data.get('authPassword'):
                password = data['authPassword']
            else:
                return Response({"error": "Password is required"}, status=status.HTTP_400_BAD_REQUEST)

            # Check if the input is an email or username
            try:
                if '@' in username_or_email:
                    author = Author.objects.get(authEmail=username_or_email)
                else:
                    author = Author.objects.get(authName=username_or_email)
            except Author.DoesNotExist:
                return Response({"error": "Invalid credentials"}, status=status.HTTP_404_NOT_FOUND)

            # Verify the password
            if check_password(password, author.authPassword):
                refresh = RefreshToken.for_user(author)
                return Response({
                    'refresh': str(refresh),
                    'access': str(refresh.access_token),
                    'authID': author.id,
                }, status=status.HTTP_200_OK)
            else:
                return Response({"error": "Invalid credentials"}, status=status.HTTP_401_UNAUTHORIZED)

        return Response({"message": "data not valid"}, status=status.HTTP_400_BAD_REQUEST)
