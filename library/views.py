# library/views.py
from .models import Loan, Book
from rest_framework import status, viewsets, permissions, generics, filters
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAdminUser
from rest_framework_simplejwt.views import TokenObtainPairView
from django.contrib.auth.models import User
from django.utils.timezone import now
from django.db import transaction
from datetime import timedelta
from .serializers import (
    BookSerializer,
    LoanSerializer,
    UserSerializer,
    CustomTokenObtainPairSerializer,
)


# Loan API (List and Manage Loans) - Requires Authentication
class LoanViewSet(viewsets.ModelViewSet):
    queryset = Loan.objects.all()
    serializer_class = LoanSerializer
    permission_classes = [permissions.IsAuthenticated]


# User Registration API
class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [AllowAny]


# Custom JWT Authentication API
class CustomTokenObtainPairView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer


# Admin Dashboard API
@api_view(["GET"])
@permission_classes([IsAdminUser])
def admin_dashboard(request):
    users_count = User.objects.count()
    books_count = Book.objects.count()
    loans_count = Loan.objects.count()

    return Response(
        {
            "users": users_count,
            "books": books_count,
            "loans": loans_count,
        }
    )


# Create a new user (Admin Only)
@api_view(["POST"])
@permission_classes([IsAdminUser])
def create_user(request):
    serializer = UserSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# Create a loan for any user (Admin Only)
@api_view(["POST"])
@permission_classes([IsAdminUser])
def create_loan(request):
    user_id = request.data.get("user_id")
    book_id = request.data.get("book_id")
    loan_type = request.data.get("loan_type")

    try:
        user = User.objects.get(id=user_id)
        book = Book.objects.get(id=book_id)

        if book.inventory <= 0:
            return Response({"error": "Book out of stock."}, status=400)

        with transaction.atomic():
            book.inventory -= 1
            book.save()

            loan_durations = {1: 10, 2: 5, 3: 2}
            return_date = now().date() + timedelta(
                days=loan_durations.get(loan_type, 10)
            )

            loan = Loan.objects.create(
                user=user,
                book=book,
                type=loan_type,
                return_date=return_date,
                returned=False,
            )

        return Response(
            {"message": "Loan created successfully!", "loan_id": loan.id}, status=201
        )
    except User.DoesNotExist:
        return Response({"error": "User not found."}, status=404)
    except Book.DoesNotExist:
        return Response({"error": "Book not found."}, status=404)


# Return any loan (Admin Only)
@api_view(["POST"])
@permission_classes([IsAdminUser])
def return_any_loan(request, loan_id):
    try:
        loan = Loan.objects.select_related("book").get(id=loan_id)

        if loan.returned:
            return Response(
                {"error": "This loan has already been returned."}, status=400
            )

        with transaction.atomic():
            loan.returned = True
            loan.save(update_fields=["returned"])
            loan.book.inventory += 1
            loan.book.save(update_fields=["inventory"])

        return Response({"message": "Loan marked as returned."}, status=200)
    except Loan.DoesNotExist:
        return Response({"error": "Loan not found."}, status=404)


# Delete a book (Admin Only)
@api_view(["DELETE"])
@permission_classes([IsAdminUser])
def delete_book(request, book_id):
    try:
        book = Book.objects.get(id=book_id)
        book.delete()
        return Response({"message": "Book deleted successfully."}, status=200)
    except Book.DoesNotExist:
        return Response({"error": "Book not found."}, status=404)


# Book API (CRUD for books) - Only Admins can Modify
class BookViewSet(viewsets.ModelViewSet):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ["name", "author", "year_published", "category"]

    def get_permissions(self):
        if self.action in ["create", "update", "partial_update", "destroy"]:
            return [permissions.IsAdminUser()]
        return [permissions.AllowAny()]


# Borrow a book (Regular Users)
@api_view(["POST"])
def borrow_book(request, book_id):
    try:
        book = Book.objects.get(id=book_id)
        overdue_loans = Loan.objects.filter(
            user=request.user, returned=False, return_date__lt=now().date()
        )
        if overdue_loans.exists():
            return Response(
                {"error": "You have overdue books. Return them before borrowing more."},
                status=400,
            )

        if book.inventory <= 0:
            return Response({"error": "This book is out of stock."}, status=400)

        with transaction.atomic():
            book.inventory -= 1
            book.save()

            loan = Loan.objects.create(
                user=request.user,
                book=book,
                type=1,  # Default loan type
                return_date=now().date() + timedelta(days=10),
                returned=False,
            )

        return Response(
            {"message": "Book borrowed successfully!", "loan_id": loan.id}, status=201
        )
    except Book.DoesNotExist:
        return Response({"error": "Book not found."}, status=404)


# Return a book (Regular Users)
@api_view(["POST"])
def return_book(request, loan_id):
    try:
        loan = Loan.objects.select_related("book").get(id=loan_id, user=request.user)

        if loan.returned:
            return Response(
                {"error": "This loan has already been returned."}, status=400
            )

        with transaction.atomic():
            loan.returned = True
            loan.save(update_fields=["returned"])
            loan.book.inventory += 1
            loan.book.save(update_fields=["inventory"])

        return Response({"message": "Book returned successfully!"}, status=200)
    except Loan.DoesNotExist:
        return Response({"error": "Loan not found."}, status=404)


# Return a loan (Regular Users)
@api_view(["POST"])
def return_loan(request, loan_id):
    try:
        loan = Loan.objects.select_related("book").get(id=loan_id, user=request.user)

        if loan.returned:
            return Response(
                {"error": "This loan has already been returned."}, status=400
            )

        with transaction.atomic():
            loan.returned = True
            loan.save(update_fields=["returned"])
            loan.book.inventory += 1
            loan.book.save(update_fields=["inventory"])

        return Response({"message": "Loan returned successfully!"}, status=200)
    except Loan.DoesNotExist:
        return Response({"error": "Loan not found."}, status=404)
