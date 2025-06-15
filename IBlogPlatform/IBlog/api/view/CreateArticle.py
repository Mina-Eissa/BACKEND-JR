from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, permissions
from rest_framework_simplejwt.authentication import JWTAuthentication
from ..models import Article, Tag
from ..serializers import ArticleSerializer, TagSerializer


class CreateArticleView(APIView):
    serializer_class = ArticleSerializer
    authentication_classes = [JWTAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, *args, **kwargs):
        tags_data = request.data.get('artTags', [])
        tags_pk = []
        tag_errors = []

        for tag in tags_data:
            tag_name = tag.get('tagName')
            if not tag_name:
                tag_errors.append({'tagName': 'This field is required.'})
                continue

            tag_instance, created = Tag.objects.get_or_create(tagName=tag_name)
            tags_pk.append(tag_instance.id)

            if created:
                tag_serializer = TagSerializer(tag_instance)
                if not tag_serializer.is_valid():
                    tag_errors.append(tag_serializer.errors)

        if tag_errors:
            return Response({'tag_errors': tag_errors}, status=status.HTTP_400_BAD_REQUEST)

        request.data['artTags'] = tags_pk
        article_serializer = self.serializer_class(data=request.data)

        if article_serializer.is_valid():
            article_serializer.save()
            return Response(article_serializer.data, status=status.HTTP_201_CREATED)

        return Response(article_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
