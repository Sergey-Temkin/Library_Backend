# library/models.py

from django.db import models
from django.contrib.auth.models import User
from django.utils.timezone import now
from datetime import timedelta
from django.core.exceptions import ValidationError

# Represents a book with attributes like name, author, year published, category, inventory count, and an optional image URL
class Book(models.Model):
    CATEGORY_CHOICES = [
        ("romance", "Romance"),
        ("action", "Action"),
        ("mystery", "Mystery"),
        ("sci-fi", "Science Fiction"),
        ("fantasy", "Fantasy"),
        ("non-fiction", "Non-Fiction"),
    ]

    name = models.CharField(max_length=255)
    author = models.CharField(max_length=255)
    year_published = models.IntegerField()
    category = models.CharField(max_length=50, choices=CATEGORY_CHOICES, default="romance")
    inventory = models.PositiveIntegerField(default=1)
    DEFAULT_IMAGE_URL = "https://png.pngtree.com/png-clipart/20230917/original/pngtree-no-image-available-icon-flatvector-illustration-thumbnail-graphic-illustration-vector-png-image_12323920.png"
    image_url = models.URLField(max_length=500, null=True, blank=True, default=DEFAULT_IMAGE_URL)

    def __str__(self):
        return f"{self.name} by: {self.author}, category: {dict(self.CATEGORY_CHOICES).get(self.category, 'Unknown')} ({self.inventory} copies available)"

# Tracks book loans with a user, book reference, loan type (duration), loan date, return date, and whether it was returned
class Loan(models.Model):
    LOAN_CHOICES = [
        (1, "10 days"), 
        (2, "5 days"), 
        (3, "2 days")
    ]
    
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    type = models.IntegerField(choices=LOAN_CHOICES)
    loan_date = models.DateField(auto_now_add=True)
    return_date = models.DateField(blank=True, null=True)
    returned = models.BooleanField(default=False)  # Tracks if book is returned

    # Override save method to update return date and decrease inventory
    def save(self, *args, **kwargs):
        # If this is a new loan and the book is out of stock, prevent saving
        if not self.pk and self.book.inventory <= 0:
            raise ValidationError(f"The book '{self.book.name}' is out of stock.")

        # If this is a new loan, set return_date and reduce the book inventory
        if not self.pk:  
            loan_durations = {1: 10, 2: 5, 3: 2}
            self.return_date = now().date() + timedelta(days=loan_durations.get(self.type, 10))
            self.book.inventory -= 1
            self.book.save()

        super().save(*args, **kwargs)  # Call the parent save method  

    # Check if the loan is overdue and not returned
    def is_overdue(self):
        return not self.returned and self.return_date < now().date()
    
    # Return a message if the loan is overdue
    def status_message(self):
        if self.is_overdue():
            return f"Overdue! Please return '{self.book.name}' immediately."
        return "Loan is active."
    
    # Mark the loan as returned and update inventory
    def return_book(self):
        if not self.returned:
            self.returned = True
            self.book.inventory += 1  # Increase book stock when returned
            self.book.save()
            self.save()
            return True  # Successful return
        return False  # Already returned

    def __str__(self):
        return f"{self.user} borrowed: {self.book} (Returned: {self.returned}, Status: {self.status_message()})"