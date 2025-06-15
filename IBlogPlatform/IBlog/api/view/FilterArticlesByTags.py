from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import permissions
from rest_framework_simplejwt.authentication import JWTAuthentication
from ..models import Article, Tag
from ..serializers import ArticleSerializer


class FilterArticlesByTagsView(APIView):
    """
    View to filter articles by tags.
    Expected input format:
    {
        "artTags": [
            {"tagName": "example_tag1"},
            {"tagName": "example_tag2"}
        ]
    }
    """
    serializer_class = ArticleSerializer
    authentication_classes = [JWTAuthentication]
    permission_classes = [permissions.IsAuthenticated]
    http_method_names = ['post']

    def post(self, request, *args, **kwargs):
        """
        Filter articles by tags.
        """
        tags_data = request.data.get('artTags', [])
        tag_names = [tag['tagName'] for tag in tags_data if 'tagName' in tag]

        if not tag_names:
            return Response({"error": "No valid tags provided."}, status=400)

        # Fetch existing tags in a single query
        existing_tags = Tag.objects.filter(tagName__in=tag_names)
        tags_exists = existing_tags.values_list('id', flat=True)

        if not tags_exists:
            return Response({"error": "No matching tags found."}, status=404)

        try:
            articles = Article.objects.filter(
                artTags__in=tags_exists).distinct().order_by('-artUpdatedAt')
            serializer = self.serializer_class(articles, many=True)
            return Response(serializer.data, status=200)
        except Exception as e:
            return Response({"error": str(e)}, status=500)
