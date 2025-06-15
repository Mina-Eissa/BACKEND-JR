from datetime import date
from django.test import TestCase
from ..models import Article, Tag, Author
from django.core.exceptions import ValidationError


class ArticleModelTest(TestCase):
    def setUp(self):
        self.author = Author.objects.create(
            authName='AuthorName',
            authEmail='john.doe@example.com',
            authBirthDate=date(1990, 1, 1),)
        self.valid_article = Article(
            artName='Valid Article',
            artContent='This is a valid article content.',
            authID=self.author,
            authName=self.author
        )
        self.invalid_article_html = Article(
            artName='Invalid Article',
            artContent='<script>alert("XSS")</script>',
            authID=self.author,
            authName=self.author
        )
        self.invalid_article_empty_content = Article(
            artName='Empty Content Article',
            artContent='',
            authID=self.author,
            authName=self.author
        )
        
    def test_valid_article_creation(self):
        self.valid_article.save()
        self.assertEqual(Article.objects.count(), 1)
        self.assertEqual(Article.objects.get(
            artName='Valid Article'), self.valid_article)

    def test_invalid_article_creation_html(self):
        with self.assertRaises(ValidationError):
            self.invalid_article_html.full_clean()

    def test_invalid_article_creation_empty_content(self):
        with self.assertRaises(ValidationError):
            self.invalid_article_empty_content.full_clean()


    def test_article_tags_relationship(self):
        tag1 = Tag.objects.create(tagName='Tag1')
        tag2 = Tag.objects.create(tagName='Tag2')
        self.valid_article.save()
        self.valid_article.artTags.add(tag1, tag2)
        self.assertEqual(self.valid_article.artTags.count(), 2)
        self.assertIn(tag1, self.valid_article.artTags.all())
        self.assertIn(tag2, self.valid_article.artTags.all())
