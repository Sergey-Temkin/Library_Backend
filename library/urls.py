# library/urls.py

from django.urls import path, include
from .views import BookViewSet, LoanViewSet, RegisterView, borrow_book
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

# Registers API routes for books, loans, user registration, login, and borrowing books
router = DefaultRouter()
router.register(r"books", BookViewSet)
router.register(r"loans", LoanViewSet)

urlpatterns = [
    path("", include(router.urls)),
    path("register/", RegisterView.as_view(), name="register"),
    path("login/", TokenObtainPairView.as_view(), name="login"), # Includes JWT authentication(Login)
    path("refresh/", TokenRefreshView.as_view(), name="refresh"), # Includes JWT authentication(Token refresh)
    path("borrow_book/<int:book_id>/", borrow_book, name="borrow_book"),
]