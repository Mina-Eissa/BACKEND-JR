from rest_framework import generics, permissions, status
from rest_framework.response import Response
from rest_framework.exceptions import NotFound
from ..serializers import PersonSerializer
from ..models import Person
from rest_framework_simplejwt.tokens import RefreshToken
import uuid


class PersonInfoView(generics.RetrieveAPIView):
    serializer_class = PersonSerializer
    queryset = Person.objects.all()
    permission_classes = [permissions.AllowAny]

    def retrieve(self, request, *args, **kwargs):
        identifier = self.kwargs.get('identifier')

        # 1.id
        try:
            uuid_id = uuid.UUID(identifier)
            person = Person.objects.get(id=uuid_id)
            serializer = self.serializer_class(person, context={'request': request})
            return Response(serializer.data, status=status.HTTP_200_OK)
        except (ValueError, Person.DoesNotExist):
            pass
        # 2.username
        try:
            person = Person.objects.get(username=identifier)
            serializer = self.serializer_class(person, context={'request': request})
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Person.DoesNotExist:
            pass

        # 3.email
        try:
            person = Person.objects.get(email=identifier)
            serializer = self.serializer_class(person, context={'request': request})
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Person.DoesNotExist:
            return Response({'NOT FOUND': 'Person not found by any value of this (id,username,email)'}, status=status.HTTP_404_NOT_FOUND)
