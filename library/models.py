# library/models.py
from django.db import models
from django.contrib.auth.models import User
from django.utils.timezone import now
from datetime import timedelta


# Represents a book with attributes like name, author, year published, category, inventory count, and an optional image URL
class Book(models.Model):
    CATEGORY_CHOICES = [
        ("Romance", "romance"),
        ("Action","action",),
        ("Mystery", "mystery"),
        ("Sci-Fi", "sci-fi"),
        ("Fantasy", "fantasy"),
        ("Non-Fiction", "non-fiction"),
    ]

    name = models.CharField(max_length=255)
    author = models.CharField(max_length=255)
    year_published = models.IntegerField()
    category = models.CharField(
        max_length=50, choices=CATEGORY_CHOICES, default="Romance"
    )
    inventory = models.PositiveIntegerField(default=1)
    DEFAULT_IMAGE_URL = "https://png.pngtree.com/png-clipart/20230917/original/pngtree-no-image-available-icon-flatvector-illustration-thumbnail-graphic-illustration-vector-png-image_12323920.png"
    image_url = models.URLField(
        max_length=500, null=True, blank=True, default=DEFAULT_IMAGE_URL
    )

    def __str__(self):
        return f"{self.name} by: {self.author}, category: {dict(self.CATEGORY_CHOICES).get(self.category, 'Unknown')} ({self.inventory} copies available)"


# Tracks book loans with a user, book reference, loan type (duration), loan date, return date, and whether it was returned
class Loan(models.Model):
    LOAN_CHOICES = [(1, "10 days"), (2, "5 days"), (3, "2 days")]

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    type = models.IntegerField(choices=LOAN_CHOICES)
    loan_date = models.DateField(auto_now_add=True)
    return_date = models.DateField(blank=True, null=True)
    returned = models.BooleanField(default=False)  # Tracks if book is returned

    def save(self, *args, **kwargs):

        if not self.return_date:  # Only set if return_date is not already provided
            loan_durations = {1: 10, 2: 5, 3: 2}  # Mapping type to days
            self.return_date = now().date() + timedelta(
                days=loan_durations.get(self.type, 10)
            )

        super().save(*args, **kwargs)  # Call parent save method

    def __str__(self):
        return f"{self.user} borrowed: {self.book} (Returned: {self.returned}, Due: {self.return_date})"
