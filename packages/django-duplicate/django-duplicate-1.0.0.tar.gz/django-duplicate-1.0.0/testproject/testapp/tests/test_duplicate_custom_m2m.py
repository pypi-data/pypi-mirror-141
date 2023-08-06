from django.test import TestCase

from testapp.factories import (
    ChildFactory,
    ParentFactory,
)
from testapp.models import (
    Child,
    ChildForParent,
    Parent,
)


class CustomM2mTestCase(TestCase):

    def test_duplicate__custom_m2m(self):
        parent = ParentFactory()
        child1 = ChildFactory()
        child2 = ChildFactory()
        ChildForParent.objects.create(parent=parent, child=child1)
        ChildForParent.objects.create(parent=parent, child=child2)

        self.assertEqual(Parent.objects.count(), 1)
        self.assertEqual(Child.objects.count(), 2)
        self.assertEqual(ChildForParent.objects.count(), 2)
        self.assertEqual(parent.children.count(), 2)

        parent_copy = parent.duplicate(paths=['children'])

        self.assertEqual(Parent.objects.count(), 2)
        self.assertEqual(Child.objects.count(), 2)
        self.assertEqual(ChildForParent.objects.count(), 4)
        self.assertEqual(parent.children.count(), 2)
        self.assertEqual(parent_copy.children.count(), 2)
