# library/tests.py

# To run test paste in terminal: python manage.py test
import os
import django
from django.contrib.auth.models import User
from django.test import TestCase
from rest_framework.test import APIClient
from rest_framework import status
from django.db import transaction
from library.models import Book, Loan

# Set up Django environment
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "library_main.settings")
django.setup()


class LibraryTestCase(TestCase):
    def setUp(self):
        """Set up test database and API client."""
        self.client = APIClient()

        # Clear all test data to avoid duplication
        Book.objects.all().delete()
        Loan.objects.all().delete()
        User.objects.all().delete()

        # Create test users
        self.user = User.objects.create_user(username="testuser", email="testuser@example.com", password="testpass")
        self.admin = User.objects.create_superuser(username="admin", email="admin@example.com", password="adminpass")

        # Create test books
        self.book = Book.objects.create(
            name="Test Book",
            author="Test Author",
            year_published=2022,
            category="action",
            inventory=5,
            image_url="https://example.com/testbook.jpg"
        )


    def authenticate_user(self):
        """Authenticate user and set token."""
        response = self.client.post("/api/library/login/", {
            "username": "testuser",
            "password": "testpass"
        })
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {response.data['access']}")

    def authenticate_admin(self):
        """Authenticate admin user and set token."""
        response = self.client.post("/api/library/login/", {
            "username": "admin",
            "password": "adminpass"
        })
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {response.data['access']}")

    def test_register_user(self):
        """Test user registration endpoint."""
        response = self.client.post("/api/library/register/", {
            "username": "newuser",
            "email": "newuser@example.com",
            "password": "newpass"
        })
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(User.objects.filter(username="newuser").exists())

    def test_get_books(self):
        """Test retrieving list of books."""
        response = self.client.get("/api/library/books/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertGreaterEqual(len(response.data), 1)

    def test_borrow_book(self):
        """Test borrowing a book."""
        self.authenticate_user()
        initial_inventory = self.book.inventory
        print(f"Initial Inventory: {initial_inventory}")

        with transaction.atomic():  # Ensure changes are committed
            response = self.client.post(f"/api/library/borrow_book/{self.book.id}/")

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        # Explicitly refresh the book instance after borrowing
        self.book.refresh_from_db()
        updated_inventory = self.book.inventory
        print(f"Updated Inventory (After Borrowing): {updated_inventory}")

        self.assertEqual(updated_inventory, initial_inventory - 1)

    def test_borrow_out_of_stock_book(self):
        """Test borrowing a book that is out of stock."""
        self.book.inventory = 0
        self.book.save()
        self.authenticate_user()
        response = self.client.post(f"/api/library/borrow_book/{self.book.id}/")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data["error"], "This book is out of stock.")

    def test_admin_create_book(self):
        """Test admin creating a book."""
        self.authenticate_admin()
        response = self.client.post("/api/library/books/", {
            "name": "New Book",
            "author": "Admin Author",
            "year_published": 2025,
            "category": "sci-fi",
            "inventory": 10,
            "image_url": "https://example.com/newbook.jpg"
        })
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(Book.objects.filter(name="New Book").exists())

    def test_unauthorized_create_book(self):
        """Test regular user cannot create a book."""
        self.authenticate_user()
        response = self.client.post("/api/library/books/", {
            "name": "Unauthorized Book",
            "author": "Unauthorized Author",
            "year_published": 2025,
            "category": "sci-fi",
            "inventory": 5,
            "image_url": "https://example.com/unauthorizedbook.jpg"
        })
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_list_loans(self):
        """Test listing all loans as an admin."""
        self.authenticate_admin()
        response = self.client.get("/api/library/loans/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_return_book(self):
        """Test returning a book."""
        self.authenticate_user()
        loan = Loan.objects.create(user=self.user, book=self.book, type=1, return_date="2025-02-20", returned=False)

        initial_inventory = self.book.inventory
        print(f"Initial Inventory (Before Return): {initial_inventory}")

        with transaction.atomic():  # Ensure database commits changes
            loan.return_book()

        # Explicitly refresh instances
        loan.refresh_from_db()
        self.book.refresh_from_db()

        updated_inventory = self.book.inventory
        print(f"Updated Inventory (After Returning): {updated_inventory}")

        self.assertTrue(loan.returned)
        self.assertEqual(updated_inventory, initial_inventory + 1)


if __name__ == "__main__":
    import unittest
    unittest.main()
