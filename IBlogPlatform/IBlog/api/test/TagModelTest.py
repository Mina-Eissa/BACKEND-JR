from django.test import TestCase
from ..models import Tag
from django.core.exceptions import ValidationError


class TagModelTest(TestCase):
    def setUp(self):
        self.valid_tag = Tag(tagName='ValidTag123')
        self.invalid_tag_special_char = Tag(tagName='Invalid@Tag')
        self.invalid_tag_space = Tag(tagName='Invalid Tag')

    def test_valid_tag_creation(self):
        self.valid_tag.save()
        self.assertEqual(Tag.objects.count(), 1)
        self.assertEqual(Tag.objects.get(
            tagName='ValidTag123'), self.valid_tag)

    def test_invalid_tag_creation_special_char(self):
        with self.assertRaises(ValidationError):
            self.invalid_tag_special_char.full_clean()

    def test_invalid_tag_creation_space(self):
        with self.assertRaises(ValidationError):
            self.invalid_tag_space.full_clean()
