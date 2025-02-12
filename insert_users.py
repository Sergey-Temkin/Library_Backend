# insert_users.py
# To insert users paste in terminal: insert_users.py
import os
import django

# Set up Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'library_main.settings')
django.setup()

from django.contrib.auth.models import User

# Define users to be added
users_data = [
    {"username": "user1", "email": "user1@example.com", "password": "user123"},
    {"username": "user2", "email": "user2@example.com", "password": "user123"},
    {"username": "user3", "email": "user3@example.com", "password": "user123"},
]

# Insert users into the database
for user_data in users_data:
    if not User.objects.filter(username=user_data["username"]).exists():
        user = User.objects.create_user(
            username=user_data["username"],
            email=user_data["email"],
            password=user_data["password"]
        )
        print(f"User {user.username} created successfully!")
    else:
        print(f"User {user_data['username']} already exists.")
