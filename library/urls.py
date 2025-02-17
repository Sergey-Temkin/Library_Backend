# library/urls.py
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import TokenRefreshView
from .views import (
    BookViewSet,
    LoanViewSet,
    RegisterView,
    CustomTokenObtainPairView,
    borrow_book,
    return_book,
    admin_dashboard,
    create_user,
    create_loan,
    return_any_loan,
    delete_book,
)


# Registers API routes for books, loans, user registration, login, and borrowing books
router = DefaultRouter()
router.register(r"books", BookViewSet)
router.register(r"loans", LoanViewSet)

urlpatterns = [
    path("", include(router.urls)),
    path("register/", RegisterView.as_view(), name="register"),
    path("login/", CustomTokenObtainPairView.as_view(), name="token_obtain_pair"),  # Includes custom JWT authentication(Login , username, is_admin)
    path("refresh/", TokenRefreshView.as_view(), name="token_refresh"),  # Includes JWT authentication(Token refresh)
    path("borrow_book/<int:book_id>/", borrow_book, name="borrow_book"),
    path("return_book/<int:loan_id>/", return_book, name="return_book"),
    path("admin-dashboard/", admin_dashboard, name="admin_dashboard"),
    path("create_user/", create_user, name="create_user"),
    path("create_loan/", create_loan, name="create_loan"),
    path("return_any_loan/<int:loan_id>/", return_any_loan, name="return_any_loan"),
    path("delete_book/<int:book_id>/", delete_book, name="delete_book"),
]
