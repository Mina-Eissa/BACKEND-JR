from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, permissions
from rest_framework_simplejwt.authentication import JWTAuthentication
from ..models import Article
from ..serializers import ArticleSerializer


class ReadArticleView(APIView):
    serializer_class = ArticleSerializer
    authentication_classes = [JWTAuthentication]
    permission_classes = [permissions.IsAuthenticated]
    allow_methods = ['GET']

    def get(self, request, *args, **kwargs):
        if request.data.get('artID'):
            artID = request.data['artID']
            try:
                article = Article.objects.get(artID=artID)
                serializer = self.serializer_class(article)
                return Response(serializer.data, status=200)
            except Article.DoesNotExist:
                return Response({'error': 'Article not found'}, status=404)

        else:
            try:
                articles = Article.objects.all().order_by('-artUpdatedAt')
                serializer = self.serializer_class(articles, many=True)
                return Response(serializer.data, status=200)
            except Article.DoesNotExist:
                return Response({'error': 'No articles found'}, status=404)
