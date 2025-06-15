
from rest_framework import viewsets, permissions
from ..models import Tag
from ..serializers import TagSerializer


class TagCRUD(viewsets.ModelViewSet):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer
