from django.urls import path, include
# (AuthorRegistration, AuthorLoggingIn,CreateArticle, ReadArticle, UpdateArticle, DeleteArticle, FilterArticlesByCreatedDate)
from .views import *

urlpatterns = [
    path("authorRegisteration/", AuthorRegistration,
         name="author-registration"),
    path("authorLoggingIn/", AuthorLoggingIn, name="author-login"),
    path("createArticle/", CreateArticle, name="create-article"),
    path("article/", ReadArticle, name='read-article_s'),
    path("updateArticle/", UpdateArticle, name='update-article'),
    path("deleteArticle/", DeleteArticle, name='delete-article'),
    path("filterArticlesByCreatedDate/", FilterArticlesByCreatedDate,
         name='filter-articles-by-created-date'),
    path("filterArticlesByTags/", FilterArticlesByTags,
         name='filter-articles-by-tags'),
]
