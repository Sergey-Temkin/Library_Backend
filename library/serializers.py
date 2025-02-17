# library/serializers.py
from .models import Book, Loan
from django.contrib.auth.models import User
from django.utils.timezone import now
from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from datetime import date, timedelta


# Custom serializer for generating JWT tokens with additional user information.
class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        token["username"] = user.username  # Include username
        token["is_admin"] = user.is_superuser  # Include admin status
        return token


# Serializes user data, including additional fields for admin management.
class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = [
            "id",
            "username",
            "email",
            "first_name",
            "last_name",
            "is_staff",
            "password",
        ]

    def create(self, validated_data):
        user = User(
            username=validated_data["username"],
            email=validated_data["email"],
            first_name=validated_data.get("first_name", ""),
            last_name=validated_data.get("last_name", ""),
            is_staff=validated_data.get(
                "is_staff", False
            ),  # Allow setting staff status
        )
        user.set_password(validated_data["password"])  # Hash the password properly
        user.save()
        return user


# Serializes and deserializes book data.
class BookSerializer(serializers.ModelSerializer):
    class Meta:
        model = Book
        fields = "__all__"


# Serializes and deserializes loan data.
class LoanSerializer(serializers.ModelSerializer):
    user_name = serializers.CharField(source="user.username", read_only=True)
    book_name = serializers.CharField(source="book.name", read_only=True)
    book_image_url = serializers.CharField(source="book.image_url", read_only=True)

    class Meta:
        model = Loan
        fields = [
            "id",
            "user",
            "user_name",
            "book",
            "book_name",
            "book_image_url",
            "type",
            "loan_date",
            "return_date",
            "returned",
        ]

    def create(self, validated_data):
        """
        Override create method to ensure `return_date` is set correctly based on loan type
        and decrease the book inventory when a loan is made.
        """
        book = validated_data["book"]
        if book.inventory <= 0:
            raise serializers.ValidationError({"error": "This book is out of stock."})

        # Reduce inventory
        book.inventory -= 1
        book.save()

        # Set return date based on loan type
        loan_type = validated_data.get("type")
        loan_durations = {1: 10, 2: 5, 3: 2}
        validated_data["return_date"] = now().date() + timedelta(
            days=loan_durations.get(loan_type, 10)
        )

        return super().create(validated_data)

    def update(self, instance, validated_data):
        """
        Override update method to allow marking books as returned.
        """
        if (
            "returned" in validated_data
            and validated_data["returned"] is True
            and not instance.returned
        ):
            instance.returned = True
            instance.book.inventory += 1  # Increase inventory when returned
            instance.book.save()

        return super().update(instance, validated_data)
