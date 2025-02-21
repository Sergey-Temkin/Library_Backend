# insert_books.py
# To insert books paste in terminal: py insert_books.py
import os
import django

# Set up Django environment
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "library_main.settings")
django.setup()

from library.models import Book
from library.serializers import BookSerializer

# List of books with real titles, authors, publication years, and cover image URLs
books_data = [
    # Romance (1 book)
    {
        "name": "Pride and Prejudice",
        "author": "Jane Austen",
        "year_published": 1813,
        "category": "Romance",
        "inventory": 1,
        "image_url": "https://upload.wikimedia.org/wikipedia/commons/thumb/1/17/PrideAndPrejudiceTitlePage.jpg/800px-PrideAndPrejudiceTitlePage.jpg",
    },
    # Action (2 books)
    {
        "name": "The Bourne Identity",
        "author": "Robert Ludlum",
        "year_published": 1980,
        "category": "Action",
        "inventory": 2,
        "image_url": "https://upload.wikimedia.org/wikipedia/en/6/65/Ludlum_-_The_Bourne_Identity_Coverart.png",
    },
    {
        "name": "The Hunger Games",
        "author": "Suzanne Collins",
        "year_published": 2008,
        "category": "Action",
        "inventory": 2,
        "image_url": "https://upload.wikimedia.org/wikipedia/en/thumb/d/dc/The_Hunger_Games.jpg/220px-The_Hunger_Games.jpg",
    },
    # Mystery (3 books)
    {
        "name": "The Girl with the Dragon Tattoo",
        "author": "Stieg Larsson",
        "year_published": 2005,
        "category": "Mystery",
        "inventory": 3,
        "image_url": "https://upload.wikimedia.org/wikipedia/en/thumb/b/bc/Thegirlwiththedragontattoo.jpg/220px-Thegirlwiththedragontattoo.jpg",
    },
    {
        "name": "Gone Girl",
        "author": "Gillian Flynn",
        "year_published": 2012,
        "category": "Mystery",
        "inventory": 3,
        "image_url": "https://upload.wikimedia.org/wikipedia/en/thumb/7/7e/Gone_Girl_%28Flynn_novel%29.jpg/220px-Gone_Girl_%28Flynn_novel%29.jpg",
    },
    {
        "name": "The Da Vinci Code",
        "author": "Dan Brown",
        "year_published": 2003,
        "category": "Mystery",
        "inventory": 3,
        "image_url": "https://upload.wikimedia.org/wikipedia/en/thumb/6/6b/DaVinciCode.jpg/220px-DaVinciCode.jpg",
    },
    # Science Fiction (1 book)
    {
        "name": "Dune",
        "author": "Frank Herbert",
        "year_published": 1965,
        "category": "Sci-Fi",
        "inventory": 1,
        "image_url": "https://upload.wikimedia.org/wikipedia/en/thumb/d/de/Dune-Frank_Herbert_%281965%29_First_edition.jpg/220px-Dune-Frank_Herbert_%281965%29_First_edition.jpg",
    },
    # Fantasy (2 books)
    {
        "name": "The Hobbit",
        "author": "J.R.R. Tolkien",
        "year_published": 1937,
        "category": "Fantasy",
        "inventory": 2,
        "image_url": "https://upload.wikimedia.org/wikipedia/en/thumb/4/4a/TheHobbit_FirstEdition.jpg/220px-TheHobbit_FirstEdition.jpg",
    },
    {
        "name": "Harry Potter and the Sorcerer’s Stone",
        "author": "J.K. Rowling",
        "year_published": 1997,
        "category": "Fantasy",
        "inventory": 2,
        "image_url": "https://upload.wikimedia.org/wikipedia/en/thumb/6/6b/Harry_Potter_and_the_Philosopher%27s_Stone_Book_Cover.jpg/220px-Harry_Potter_and_the_Philosopher%27s_Stone_Book_Cover.jpg",
    },
    # Non-Fiction (3 books)
    {
        "name": "Sapiens: A Brief History of Humankind",
        "author": "Yuval Noah Harari",
        "year_published": 2011,
        "category": "Non-Fiction",
        "inventory": 3,
        "image_url": "https://upload.wikimedia.org/wikipedia/en/thumb/0/06/%E1%B8%B2itsur_toldot_ha-enoshut.jpg/220px-%E1%B8%B2itsur_toldot_ha-enoshut.jpg",
    },
    {
        "name": "The Power of Habit",
        "author": "Charles Duhigg",
        "year_published": 2012,
        "category": "Non-Fiction",
        "inventory": 3,
        "image_url": "https://upload.wikimedia.org/wikipedia/en/thumb/7/7f/The_Power_of_Habit.jpg/220px-The_Power_of_Habit.jpg",
    },
    {
        "name": "Educated: A Memoir",
        "author": "Tara Westover",
        "year_published": 2018,
        "category": "Non-Fiction",
        "inventory": 3,
        "image_url": "https://upload.wikimedia.org/wikipedia/en/thumb/1/1f/Educated_%28Tara_Westover%29.png/220px-Educated_%28Tara_Westover%29.png",
    },
]
# Insert books into the database
for book_data in books_data:
    try:
        book, created = Book.objects.get_or_create(name=book_data["name"], defaults=book_data)
        if created:
            print(f"✅ Book '{book_data['name']}' added successfully!")
        else:
            print(f"⚠️ Book '{book_data['name']}' already exists, skipping.")
    except Exception as e:
        print(f"❌ Error adding book '{book_data['name']}': {e}")

print("🎉 Book insertion completed!")
