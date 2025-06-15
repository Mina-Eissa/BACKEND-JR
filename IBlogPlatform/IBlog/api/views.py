from .view.AuthorRegisteration import AuthorRegistrationView
from .view.AuthorLoggingIn import AuthorLoggingInView
from .view.CreateArticle import CreateArticleView
from .view.ReadArticle import ReadArticleView
from .view.UpdateArticle import UpdateArticleView
from .view.DeleteArticle import DeleteArticleView
from .view.FilterArticlesByCreatedDate import FilterArticlesByCreatedDateView
from .view.FilterArticlesByTags import FilterArticlesByTagsView

AuthorRegistration = AuthorRegistrationView.as_view()
AuthorLoggingIn = AuthorLoggingInView.as_view()
CreateArticle = CreateArticleView.as_view()
ReadArticle = ReadArticleView.as_view()
UpdateArticle = UpdateArticleView.as_view()
DeleteArticle = DeleteArticleView.as_view()
FilterArticlesByCreatedDate = FilterArticlesByCreatedDateView.as_view()
FilterArticlesByTags = FilterArticlesByTagsView.as_view()
