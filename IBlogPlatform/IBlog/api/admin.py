from django.contrib import admin
from .models import Author, Tag, Article

admin.site.register(Author)
admin.site.register(Tag)
admin.site.register(Article)
