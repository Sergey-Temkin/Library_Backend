# insert_users.py
# To insert users, run in terminal: python insert_users.py

import os
import django

# Set up Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'library_main.settings')
django.setup()

from django.contrib.auth.models import User

# Define users to be added
users_data = [
    {"username": "user1", "email": "user1@example.com", "password": "user1", "first_name": "user1", "last_name": "user1", "is_staff": False},
    {"username": "user2", "email": "user2@example.com", "password": "user2", "first_name": "user2", "last_name": "user2", "is_staff": False},
    {"username": "user3", "email": "user3@example.com", "password": "user3", "first_name": "user3", "last_name": "user3", "is_staff": False},
]


# Insert users into the database
for user_data in users_data:
    try:
        user, created = User.objects.get_or_create(username=user_data["username"], defaults={
            "email": user_data["email"],
            "first_name": user_data["first_name"],
            "last_name": user_data["last_name"],
            "is_staff": user_data["is_staff"]
        })

        if created:
            user.set_password(user_data["password"])  # Properly hash the password
            user.save()
            print(f"✅ User '{user.username}' created successfully!")
        else:
            print(f"⚠️ User '{user.username}' already exists, skipping.")
    except Exception as e:
        print(f"❌ Error creating user '{user_data['username']}': {e}")

print("🎉 User insertion completed!")
