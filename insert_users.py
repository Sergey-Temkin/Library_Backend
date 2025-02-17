# insert_users.py
# To insert users paste in terminal: py insert_users.py
import os
import django

# Set up Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'library_main.settings')
django.setup()

from django.contrib.auth.models import User
from library.serializers import UserSerializer

# Define users to be added( ********* is not the password)
users_data = [
    {"username": "Tal", "email": "Tal@example.com", "password": "*********", "first_name": "Tal", "last_name": "Cohen", "is_staff": False},
    {"username": "Gal", "email": "Gal@example.com", "password": "*********", "first_name": "Gal", "last_name": "Levi", "is_staff": False},
    {"username": "Ben", "email": "Ben@example.com", "password": "*********", "first_name": "Ben", "last_name": "Shimon", "is_staff": False},
]
# Insert users into the database
for user_data in users_data:
    if not User.objects.filter(username=user_data["username"]).exists():
        serializer = UserSerializer(data=user_data)
        if serializer.is_valid():
            serializer.save()
            print(f"User {user_data['username']} created successfully!")
        else:
            print(f"Error creating user {user_data['username']}: {serializer.errors}")
    else:
        print(f"User {user_data['username']} already exists.")