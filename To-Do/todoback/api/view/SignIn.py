from rest_framework import generics, permissions, status
from rest_framework.response import Response
from ..serializers import PersonSerializer
from ..models import Person
from rest_framework_simplejwt.tokens import RefreshToken


class SignInView(generics.RetrieveAPIView):
    serializer_class = PersonSerializer
    queryset = Person.objects.all()
    permission_classes = [permissions.AllowAny]

    def post(self, request, *args, **kwargs):
        identifier = self.kwargs.get('identifier')
        password = request.data.get('password')
        # 1.username
        try:
            person = Person.objects.get(username=identifier)
            if not person.check_password(password):
                return Response({'error': 'Password invalid'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
            serilaizer = self.serializer_class(person,context={'request': request})
            refresh_token = RefreshToken.for_user(user=person)
            return Response({
                'Person': serilaizer.data,
                'refresh_token': str(refresh_token),
                'access_token': str(refresh_token.access_token)
            }, status=status.HTTP_200_OK)
        except Person.DoesNotExist:
            pass

        # 2.email
        try:
            person = Person.objects.get(email=identifier)
            if not person.check_password(password):
                return Response({'error': 'Password invalid'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
            serilaizer = self.serializer_class(person, context={'request': request})
            refresh_token = RefreshToken.for_user(user=person)
            return Response({
                'Person': serilaizer.data,
                'refresh_token': str(refresh_token),
                'access_token': str(refresh_token.access_token)
            }, status=status.HTTP_200_OK)
        except Person.DoesNotExist:
            return Response({'NOT FOUND': 'Person not found by any value of this (username,email)'}, status=status.HTTP_404_NOT_FOUND)
