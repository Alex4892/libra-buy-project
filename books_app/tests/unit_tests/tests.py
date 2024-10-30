from django.test import TestCase, RequestFactory
from django.contrib.auth import get_user_model
from django.urls import reverse

from books_app.models import Genre, Book
from books_app.forms import BookForm

User = get_user_model()

class BookViewTests(TestCase):
    def setUp(self):
        self.factory = RequestFactory()
        self.user = User.objects.create_user(
            username='testuser',
            password='password'
        )
        self.genre = Genre.objects.create(name="Test Genre")
        self.book = Book.objects.create(
            name='Test Book',
            author='Test Author',
            description='Test Desc',
            publication_year=2023,
            price=199.99,
            quantity=10,
            seller=self.user
        )
        self.book.genre.add(self.genre)
    
    def test_view_books(self):
        url = reverse('books:index')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'books/index.html')
        self.assertIn('books', response.context)
        self.assertEqual(len(response.context['books']), 1)

    def test_view_detail_book(self):
        url = reverse('books:detail_book', args=[self.book.id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'books/detail_book.html')
        self.assertIn('book', response.context)
        self.assertEqual(response.context['book'].name, 'Test Book')
    
    def test_add_book_view_get(self):
        url = reverse('books:add_book')
        self.client.login(username='testuser', password='password')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'books/add_book.html')
        self.assertIsInstance(response.context['form'], BookForm)
    
    def test_add_book_view_post(self):
        url = reverse('books:add_book')
        data = {
            'name': 'New Test Book',
            'author': 'New Test Author',
            'description': 'New Test Desc',
            'publication': 'New Publication',
            'publication_year': 2023,
            'price': 199.99,
            'quantity': 10,
            'genre': [self.genre.id]
        }
        self.client.login(username='testuser', password='password')
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(Book.objects.filter(name="New Test Book").count(), 1)

# python manage.py test books_app.tests.unit_tests.tests