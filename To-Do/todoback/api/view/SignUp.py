from rest_framework import generics,permissions
from rest_framework.response import Response
from ..serializers import PersonSerializer
from ..models import Person
from rest_framework_simplejwt.tokens import RefreshToken


class SignUpView(generics.CreateAPIView):
    """
    API view to handle user sign up.
    """
    serializer_class = PersonSerializer
    queryset = Person.objects.all()
    permission_classes = [permissions.AllowAny]
    # authentication_classes = []

    def create(self, request, *args, **kwargs):
        """
        Handle user sign up.
        """
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        refresh_token = RefreshToken.for_user(serializer.instance)
        return Response({
            "status": "success",
            "refresh_token": str(refresh_token),
            "access_token": str(refresh_token.access_token),
            "data": serializer.data
        }, status=201)
