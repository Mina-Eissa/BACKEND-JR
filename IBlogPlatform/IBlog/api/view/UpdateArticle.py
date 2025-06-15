from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, permissions
from rest_framework_simplejwt.authentication import JWTAuthentication
from ..models import Article, Tag
from ..serializers import ArticleSerializer, TagSerializer


class UpdateArticleView(APIView):
    serializer_class = ArticleSerializer
    authentication_classes = [JWTAuthentication]
    permission_classes = [permissions.IsAuthenticated]
    http_method_names = ['post', 'put']

    def post(self, request, *args, **kwargs):
        art_id = request.data.get('artID')
        if not art_id:
            return Response({'error': 'You should provide artID'}, status=400)

        try:
            article = Article.objects.get(artID=art_id)
        except Article.DoesNotExist:
            return Response({'error': 'This Article does not exist'}, status=404)

        # Handling Tags: create non-existing Tags and set PK for artTags
        tags_data = request.data.get('artTags', [])
        tags_pk = []
        existing_tags = {tag.tagName: tag.id for tag in Tag.objects.all()}

        for tag in tags_data:
            tag_name = tag.get('tagName')
            if tag_name in existing_tags:
                tags_pk.append(existing_tags[tag_name])
            else:
                tag_serializer = TagSerializer(data=tag)
                if tag_serializer.is_valid():
                    tag_instance = tag_serializer.save()
                    tags_pk.append(tag_instance.id)
                else:
                    return Response(tag_serializer.errors, status=400)

        request.data['artTags'] = tags_pk
        serializer = ArticleSerializer(article, data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=200)

        return Response(serializer.errors, status=400)
