# library/admin.py
from django.contrib import admin
from django.contrib.auth.models import User
from django.contrib.auth.admin import UserAdmin
from django.forms import ValidationError
from .models import Book, Loan

# Register User model in Django Admin
if not admin.site.is_registered(User):

    @admin.register(User)
    class CustomUserAdmin(UserAdmin):
        list_display = (
            "username",
            "email",
            "first_name",
            "last_name",
            "is_staff",
            "is_active",
        )
        search_fields = ("username", "email")
        list_filter = ("is_staff", "is_active")


# Book Management in Admin Panel
@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "author",
        "year_published",
        "category",
        "inventory",
        "image_url",
    )
    search_fields = ("name", "author")
    list_filter = ("category", "year_published")
    readonly_fields = []  # Remove inventory from readonly fields


# Loan Management in Admin Panel
from django.core.exceptions import ValidationError


@admin.register(Loan)
class LoanAdmin(admin.ModelAdmin):
    list_display = ("user", "book", "loan_date", "return_date", "returned")
    list_filter = ("returned", "loan_date", "return_date")
    search_fields = ("user__username", "book__name")

    def save_model(self, request, obj, form, change):
        if not change:  # New loan is being created
            if obj.book.inventory <= 0:
                raise ValidationError("This book is out of stock.")

            obj.book.inventory -= 1  # Reduce inventory when loan is made
            obj.book.save(update_fields=["inventory"])

        else:  # If modifying an existing loan
            old_loan = Loan.objects.get(pk=obj.pk)

            # Prevent accidental modification of loan dates
            if (
                old_loan.loan_date != obj.loan_date
                or old_loan.return_date != obj.return_date
            ):
                raise ValidationError("Loan date and return date cannot be changed.")

            if not old_loan.returned and obj.returned:  # Marking as returned
                obj.book.inventory += 1
                obj.book.save(update_fields=["inventory"])

        super().save_model(request, obj, form, change)
