# library/tests.py
# To run test paste in terminal: python manage.py test
from django.test import TestCase
from django.contrib.auth.models import User
from .models import Book, Loan
from django.utils.timezone import now
from datetime import timedelta
from rest_framework.test import APIClient
from rest_framework import status


class LibraryTestCase(TestCase):
    def setUp(self):
        # Create an admin user
        self.admin_user = User.objects.create_superuser(
            username="admin", email="admin@example.com", password="adminpass"
        )
        self.client = APIClient()
        self.client.force_authenticate(user=self.admin_user)

        # Create a regular user
        self.user = User.objects.create_user(
            username="testuser", email="test@example.com", password="password123"
        )

        # Create a book
        self.book = Book.objects.create(
            name="Test Book",
            author="Author Name",
            year_published=2020,
            category="Action",
            inventory=5,
        )

    def test_admin_dashboard(self):
        response = self.client.get("/api/library/admin-dashboard/")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data["users"], 2)
        self.assertEqual(response.data["books"], 1)
        self.assertEqual(response.data["loans"], 0)

    def test_create_user(self):
        data = {
            "username": "newuser",
            "email": "newuser@example.com",
            "password": "newpassword",
            "first_name": "First",
            "last_name": "Last",
            "is_staff": False,
        }
        response = self.client.post("/api/library/create_user/", data)
        self.assertEqual(response.status_code, 201)
        self.assertTrue(User.objects.filter(username="newuser").exists())

    def test_create_book(self):
        data = {
            "name": "Another Book",
            "author": "New Author",
            "year_published": 2022,
            "category": "Fantasy",
            "inventory": 3,
        }
        response = self.client.post("/api/library/books/", data)
        self.assertEqual(response.status_code, 201)
        self.assertTrue(Book.objects.filter(name="Another Book").exists())

    def test_delete_book(self):
        response = self.client.delete(f"/api/library/delete_book/{self.book.id}/")
        self.assertEqual(response.status_code, 200)
        self.assertFalse(Book.objects.filter(id=self.book.id).exists())

    def test_create_loan(self):
        data = {
            "user_id": self.user.id,
            "book_id": self.book.id,
            "loan_type": 1,  # 10-day loan
        }
        response = self.client.post("/api/library/create_loan/", data)
        self.assertEqual(response.status_code, 201)
        self.assertTrue(Loan.objects.filter(user=self.user, book=self.book).exists())

        # Check inventory decrement
        self.book.refresh_from_db()
        self.assertEqual(self.book.inventory, 4)

    def test_return_loan(self):
        loan = Loan.objects.create(
            user=self.user, book=self.book, type=1, returned=False
        )
        response = self.client.post(f"/api/library/return_any_loan/{loan.id}/")
        self.assertEqual(response.status_code, 200)
        loan.refresh_from_db()
        self.assertTrue(loan.returned)

        # Check inventory increment
        self.book.refresh_from_db()
        self.assertEqual(self.book.inventory, 6)

    def test_loan_return_date_auto_set(self):
        loan = Loan.objects.create(user=self.user, book=self.book, type=2)  # 5-day loan
        self.assertEqual(loan.return_date, now().date() + timedelta(days=5))
