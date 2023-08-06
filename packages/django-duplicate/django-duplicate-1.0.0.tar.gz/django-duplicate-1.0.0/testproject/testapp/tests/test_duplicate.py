from django.test import TestCase

from testapp.factories import (
    AuthorFactory,
    BookFactory,
)
from testapp.models import (
    Author,
    Book,
)


class DuplicateMixinTestCase(TestCase):

    def test_duplicate(self):
        author = AuthorFactory()

        self.assertEqual(Author.objects.count(), 1)

        author_copy = author.duplicate()

        self.assertNotEqual(author.pk, author_copy.pk)
        self.assertEqual(author.name, author_copy.name)

        self.assertEqual(Author.objects.count(), 2)

    def test_duplicate__override_fields(self):
        author = AuthorFactory(name='Author name')

        self.assertEqual(Author.objects.count(), 1)

        author_copy = author.duplicate(override_fields={
            'name': 'New name'
        })

        self.assertNotEqual(author.pk, author_copy.pk)
        self.assertEqual(author.name, 'Author name')
        self.assertEqual(author_copy.name, 'New name')

        self.assertEqual(Author.objects.count(), 2)

    def test_duplicate__with_foreign_key(self):
        book = BookFactory()

        self.assertEqual(Book.objects.count(), 1)
        self.assertEqual(Author.objects.count(), 1)

        book_copy = book.duplicate(paths=['author'])

        self.assertNotEqual(book.pk, book_copy.pk)
        self.assertNotEqual(book.author_id, book_copy.author_id)
        self.assertEqual(book.title, book_copy.title)
        self.assertEqual(book.author.name, book_copy.author.name)

        self.assertEqual(Book.objects.count(), 2)
        self.assertEqual(Author.objects.count(), 2)

    def test_duplicate__exclude_models(self):
        book = BookFactory()

        self.assertEqual(Book.objects.count(), 1)
        self.assertEqual(Author.objects.count(), 1)

        book_copy = book.duplicate(paths=[])

        self.assertNotEqual(book.pk, book_copy.pk)
        self.assertEqual(book.author_id, book_copy.author_id)
        self.assertEqual(book.title, book_copy.title)

        self.assertEqual(Book.objects.count(), 2)
        self.assertEqual(Author.objects.count(), 1)
