from django.core.exceptions import ValidationError
from django.test import TestCase
from django.utils import timezone
from ..models import Author
from datetime import date


class AuthorModelTest(TestCase):

    def setUp(self):
        """Create an Author instance for testing."""
        self.author = Author.objects.create(
            authName='JohnDoe',
            authEmail='john.doe@example.com',
            authBirthDate=date(1990, 1, 1),
            authBio='This is a test bio.',
            authPassword='hashed_password'  # Assume this is a hashed password
        )

    def test_author_creation(self):
        """Test that the author is created correctly."""
        self.assertEqual(self.author.authName, 'JohnDoe')
        self.assertEqual(self.author.authEmail, 'john.doe@example.com')
        self.assertEqual(self.author.authBio, 'This is a test bio.')

    def test_author_age(self):
        """Test the age calculation."""
        expected_age = timezone.now().year - 1990  # Assuming the current year is 2023
        self.assertEqual(self.author.age, expected_age)

    def test_author_str(self):
        """Test the string representation of the author."""
        self.assertEqual(str(self.author), 'JohnDoe')

    def test_auth_img_default(self):
        """Test that the default image is set correctly."""
        self.assertEqual(self.author.authImg, 'images/default_personal.png')

    def test_auth_wallpaper_default(self):
        """Test that the default wallpaper is set correctly."""
        self.assertEqual(self.author.authWallpaper,
                         'images/default_wallpaper.png')

    def test_auth_bio_validation(self):
        """Test that the bio validation works."""
        # Test with a valid bio
        try:
            self.author.full_clean()  # This should not raise an error
        except ValidationError:
            self.fail("ValidationError raised unexpectedly for a valid bio.")

        # Test with an invalid bio (e.g., containing HTML)
        self.author.authBio = '<script>alert("XSS")</script>'  # Invalid bio
        with self.assertRaises(ValidationError):
            self.author.full_clean()  # This should raise a ValidationError