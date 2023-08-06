from django.test import TestCase

from testapp.factories import (
    DocumentFactory,
)
from testapp.models import (
    Document,
)


class DuplicateModelsWithFilesTestCase(TestCase):

    def test_duplicate__file_field(self):
        doc = DocumentFactory()
        self.assertIsNotNone(doc.file)
        self.assertEqual(Document.objects.count(), 1)

        doc_copy = doc.duplicate()
        self.assertNotEqual(doc.pk, doc_copy.pk)
        self.assertIsNotNone(doc_copy.file)
        self.assertNotEqual(doc.file, doc_copy.file)

        self.assertEqual(Document.objects.count(), 2)
