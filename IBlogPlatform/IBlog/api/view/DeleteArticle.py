from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, permissions
from rest_framework_simplejwt.authentication import JWTAuthentication
from ..models import Article, Tag
from ..serializers import ArticleSerializer, TagSerializer


class DeleteArticleView(APIView):
    serializer_class = ArticleSerializer
    authentication_classes = [JWTAuthentication]
    permission_classes = [permissions.IsAuthenticated]
    allowed_methods = ['DELETE']

    def delete(self, request, *args, **kwargs):
        article_id = request.data.get('artID')

        if not article_id:
            return Response({"error": "Article ID 'artID' is required."}, status=status.HTTP_400_BAD_REQUEST)
        try:
            article = Article.objects.get(artID=article_id)
            article.delete()
            return Response({"message": "Article deleted successfully."}, status=status.HTTP_204_NO_CONTENT)
        except Article.DoesNotExist:
            return Response({"error": "Article not found."}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            # Handle other exceptions
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
