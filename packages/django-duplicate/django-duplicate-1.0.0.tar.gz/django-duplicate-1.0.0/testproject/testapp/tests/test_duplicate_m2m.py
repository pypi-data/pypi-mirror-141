from django.apps import apps
from django.db.utils import IntegrityError
from django.test import TestCase

from testapp.factories import (
    BookFactory,
    LibraryFactory,
)
from testapp.models import (
    Author,
    Book,
    Library,
)


class DuplicateM2MTestCase(TestCase):

    def test_duplicate_m2m(self):
        LibraryBooksModel = apps.get_model('duplicate', 'Library_books')

        book1 = BookFactory()
        book2 = BookFactory()
        library = LibraryFactory()
        library.books.add(book1)
        library.books.add(book2)

        self.assertEqual(Book.objects.count(), 2)
        self.assertEqual(Author.objects.count(), 2)
        self.assertEqual(Library.objects.count(), 1)
        self.assertEqual(LibraryBooksModel.objects.count(), 2)
        self.assertEqual(library.books.count(), 2)

        library_copy = library.duplicate(paths=['books'])

        self.assertEqual(Library.objects.count(), 2)
        self.assertEqual(library.books.count(), 2)
        self.assertEqual(library_copy.books.count(), 2)

        self.assertEqual(LibraryBooksModel.objects.count(), 4)

        self.assertEqual(Book.objects.count(), 2)
        self.assertEqual(Author.objects.count(), 2)
