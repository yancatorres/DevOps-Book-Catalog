from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from .models import Book


class BookAPITest(APITestCase):

    def setUp(self):
        self.book = Book.objects.create(
            title="Harry Potter",
            author="J. K. Rowling",
            isbn="9781408855652",
            published_date="2026-07-30"
        )
        self.url = reverse('book-list')

    def test_get_books(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_create_book(self):
        data = {
            "title": "The Hobbit",
            "author": "J. R. R. Tolkien",
            "isbn": "9780261103344",
            "published_date": "1937-09-21"
        }

        response = self.client.post(self.url, data)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Book.objects.count(), 2)

    def test_update_book(self):
        url = reverse('book-detail', args=[self.book.id])

        data = {
            "title": "Harry Potter Updated",
            "author": "J. K. Rowling",
            "isbn": "9781408855652",
            "published_date": "2026-07-30"
        }

        response = self.client.put(url, data)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.book.refresh_from_db()
        self.assertEqual(self.book.title, "Harry Potter Updated")