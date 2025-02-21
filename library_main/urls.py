# library_main/urls.py
from django.contrib import admin
from django.urls import path, include

# Includes Django admin and library API endpoints
urlpatterns = [
    path("admin/", admin.site.urls), # Django Admin access
    path("api/library/", include("library.urls")), # Your Django API endpoints
]
