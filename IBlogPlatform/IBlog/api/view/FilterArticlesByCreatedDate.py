from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import permissions
from rest_framework_simplejwt.authentication import JWTAuthentication
from ..models import Article
from ..serializers import ArticleSerializer
from datetime import datetime, timedelta


class FilterArticlesByCreatedDateView(APIView):
    """
    View to filter articles by created date.
    Expected input format:
    {
        "startDate": "YYYY-MM-DD",
        "endDate": "YYYY-MM-DD"
    }
    """
    serializer_class = ArticleSerializer
    authentication_classes = [JWTAuthentication]
    permission_classes = [permissions.IsAuthenticated]
    http_method_names = ['post']

    def post(self, request, *args, **kwargs):
        """
        Filter articles by created date.
        """
        start_date = request.data.get('startDate')
        end_date = request.data.get('endDate')

        if not start_date:
            return Response({"error": "startDate is required."}, status=400)
        if not end_date:
            return Response({"error": "endDate is required."}, status=400)

        try:
            # Parse the dates
            start_date = datetime.strptime(start_date, "%Y-%m-%d")
            end_date = datetime.strptime(end_date, "%Y-%m-%d")

            # Ensure end_date is inclusive
            end_date += timedelta(days=1)

            articles = Article.objects.filter(artCreatedAt__range=(
                start_date, end_date)).order_by('-artCreatedAt')
            serializer = self.serializer_class(articles, many=True)

            if not articles.exists():
                return Response({"message": "No articles found for the given date range."}, status=404)

            return Response(serializer.data, status=200)

        except ValueError as ve:
            return Response({"error": f"Invalid date format: {str(ve)}"}, status=400)
        except Exception as e:
            return Response({"error": str(e)}, status=500)
