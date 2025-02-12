# library/views.py

from .models import Loan, Book
from .serializers import BookSerializer, LoanSerializer, UserSerializer
from rest_framework import status, viewsets, permissions,generics,filters
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from django.contrib.auth.models import User
from django.utils.timezone import now 
from datetime import timedelta

# API view for listing, searching, and managing books (CRUD). Admin-only for modifications
class BookViewSet(viewsets.ModelViewSet):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ["name", "author", "year_published", "category"]

    def get_permissions(self):
        if self.action in ["create", "update", "partial_update", "destroy"]:
            return [permissions.IsAdminUser()]
        return [permissions.AllowAny()]

# API view for managing loans, requiring authentication
class LoanViewSet(viewsets.ModelViewSet):
    queryset = Loan.objects.all()
    serializer_class = LoanSerializer
    permission_classes = [permissions.IsAuthenticated]

# API endpoint for user registration
class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [AllowAny]


@api_view(["POST"])
# Handles borrowing a book, checks stock and overdue loans, then updates inventory
def borrow_book(request, book_id):
    try:
        book = Book.objects.get(id=book_id)

        # Check if the user has any overdue loans
        overdue_loans = Loan.objects.filter(user=request.user, returned=False, return_date__lt=now().date())
        if overdue_loans.exists():
            return Response({"error": "You have overdue books. Return them before borrowing more."}, status=400)

        # Check if the book is available
        if book.inventory <= 0:
            return Response({"error": "This book is out of stock."}, status=400)

        # Create the loan - inventory is updated inside Loan.save()
        Loan.objects.create(user=request.user, book=book, type=1, return_date=now().date() + timedelta(days=10))

        return Response({"message": "Book borrowed successfully!"}, status=201)

    except Book.DoesNotExist:
        return Response({"error": "Book not found."}, status=404)