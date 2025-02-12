# library/admin.py

from django.contrib import admin
from .models import Book, Loan

# Defines how books are displayed and searched in the admin interface
@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    list_display = ("name", "author", "year_published", "category", "inventory", "image_url")
    search_fields = ("name", "author")
    list_filter = ("category", "year_published")

# Registers the Loan model in the Django Admin panel
@admin.register(Loan)
class LoanAdmin(admin.ModelAdmin):
    list_display = ("user", "book", "loan_date", "return_date", "returned")

    def save_model(self, request, obj, form, change):
        """
        When updating the 'returned' field from admin,
        increase book inventory if it is marked as returned.
        """
        if change:  # If modifying an existing Loan
            old_loan = Loan.objects.get(pk=obj.pk)
            if not old_loan.returned and obj.returned:  # Just marked as returned
                obj.book.inventory += 1
                obj.book.save()

        super().save_model(request, obj, form, change)

    def delete_model(self, request, obj):
        """
        When deleting a loan from admin, return the book to inventory.
        """
        if not obj.returned:
            obj.book.inventory += 1
            obj.book.save()
        
        super().delete_model(request, obj)
