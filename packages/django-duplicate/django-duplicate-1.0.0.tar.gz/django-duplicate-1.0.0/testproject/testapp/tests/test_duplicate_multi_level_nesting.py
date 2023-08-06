from django.test import TestCase

from duplicate.duplicates import NestedM2MOverride
from duplicate.utils import CallableValue

from testapp.factories import (
    BookFactory,
    BuildingFactory,
    CartFactory,
    ClientFactory,
    LibraryFactory,
    PriorityCartFactory,
    ProductFactory,
    ProductInCartFactory,
)
from testapp.models import (
    Book,
    Building,
    Cart,
    Client,
    Library,
    PriorityCart,
    Product,
    ProductInCart,
)


class MultiLevelNestingTestCase(TestCase):

    def test_duplicate__multiple_level_nesting(self):
        book1 = BookFactory()
        book2 = BookFactory()
        library = LibraryFactory()  # type: Library
        library.books.add(book1)
        library.books.add(book2)
        building = BuildingFactory(library=library)  # type: Building
        building.previous_building = BuildingFactory(previous_building=building, library=None)
        building.save()
        library.nearest_building = building
        library.save()

        building_copy = building.duplicate(paths=['library.nearest_building', 'library.books', 'previous_building'])
        building_copy = Building.objects.get(pk=building_copy.pk)

        self.assertEqual(Building.objects.count(), 4)
        self.assertEqual(Library.objects.count(), 2)
        self.assertEqual(Book.objects.count(), 2)
        self.assertEqual(building.library.books.count(), 2)
        self.assertEqual(building_copy.library.books.count(), 2)
        self.assertNotEqual(building.library, building_copy.library)
        self.assertNotEqual(building.library.nearest_building, building_copy.library.nearest_building)
        self.assertNotEqual(building.previous_building, building_copy.previous_building)

    def test_duplicate__multiple_level_nesting__copy_only_some_paths(self):
        book1 = BookFactory()
        book2 = BookFactory()
        library = LibraryFactory()  # type: Library
        library.books.add(book1)
        library.books.add(book2)
        building = BuildingFactory(library=library)  # type: Building
        building.previous_building = BuildingFactory(previous_building=building, library=None)
        building.save()
        library.nearest_building = building
        library.save()

        building_copy = building.duplicate(paths=['library.books'])
        building_copy = Building.objects.get(pk=building_copy.pk)

        self.assertEqual(Building.objects.count(), 3)
        self.assertEqual(Library.objects.count(), 2)
        self.assertEqual(Book.objects.count(), 2)
        self.assertEqual(building.library.books.count(), 2)
        self.assertEqual(building_copy.library.books.count(), 2)
        self.assertNotEqual(building.library, building_copy.library)
        self.assertEqual(building.previous_building, building_copy.previous_building)
        self.assertEqual(building.library.nearest_building, building_copy.library.nearest_building)

    def test_duplicate__multiple_level_nesting__single_level_deep_copy(self):
        book1 = BookFactory()
        book2 = BookFactory()
        library = LibraryFactory()  # type: Library
        library.books.add(book1)
        library.books.add(book2)
        building = BuildingFactory(library=library)  # type: Building
        building.previous_building = BuildingFactory(previous_building=building, library=None)
        building.save()
        library.nearest_building = building
        library.save()

        building_copy = building.duplicate(paths=['*'])
        building_copy = Building.objects.get(pk=building_copy.pk)

        self.assertEqual(Building.objects.count(), 4)
        self.assertEqual(Library.objects.count(), 2)
        self.assertEqual(Book.objects.count(), 2)
        self.assertEqual(building.library.books.count(), 2)
        self.assertEqual(building_copy.library.books.count(), 0)
        self.assertNotEqual(building.library, building_copy.library)
        self.assertNotEqual(building.previous_building, building_copy.previous_building)
        self.assertEqual(building.library.nearest_building, building_copy.library.nearest_building)

    def test_duplicate__multiple_level_nesting__shallow_copy_one_path(self):
        book1 = BookFactory()
        book2 = BookFactory()
        library = LibraryFactory()  # type: Library
        library.books.add(book1)
        library.books.add(book2)
        building = BuildingFactory(library=library)  # type: Building
        building.previous_building = BuildingFactory(previous_building=building, library=None)
        building.save()
        library.nearest_building = building
        library.save()

        building_copy = building.duplicate(paths=['library'])
        building_copy = Building.objects.get(pk=building_copy.pk)

        self.assertEqual(Building.objects.count(), 3)
        self.assertEqual(Library.objects.count(), 2)
        self.assertEqual(Book.objects.count(), 2)
        self.assertEqual(building.library.books.count(), 2)
        self.assertEqual(building_copy.library.books.count(), 0)
        self.assertNotEqual(building.library, building_copy.library)
        self.assertEqual(building.previous_building, building_copy.previous_building)
        self.assertEqual(building.library.nearest_building, building_copy.library.nearest_building)

    def test_duplicate__multiple_level_nesting__shallow_copy_one_path_with_duplicate_reference(self):
        book1 = BookFactory()
        book2 = BookFactory()
        library = LibraryFactory()  # type: Library
        library.books.add(book1)
        library.books.add(book2)
        building = BuildingFactory(library=library)  # type: Building
        building.previous_building = BuildingFactory(previous_building=building, library=None)
        building.save()
        library.nearest_building = building
        library.save()

        building_copy = building.duplicate(paths=['library.~'])
        building_copy = Building.objects.get(pk=building_copy.pk)

        self.assertEqual(Building.objects.count(), 3)
        self.assertEqual(Library.objects.count(), 2)
        self.assertEqual(Book.objects.count(), 2)
        self.assertEqual(building.library.books.count(), 2)
        self.assertEqual(building_copy.library.books.count(), 0)
        self.assertNotEqual(building.library, building_copy.library)
        self.assertEqual(building.previous_building, building_copy.previous_building)
        self.assertNotEqual(building.library.nearest_building, building_copy.library.nearest_building)
        self.assertEqual(building_copy.library.nearest_building, building_copy)

    def test_duplicate__multiple_level_nesting__custom_m2m(self):
        product1 = ProductFactory()
        product2 = ProductFactory()
        cart = CartFactory()
        ProductInCartFactory(cart=cart, product=product1)
        ProductInCartFactory(cart=cart, product=product2)
        client = ClientFactory(cart=cart)

        client_copy = client.duplicate(paths=['cart.products'])

        self.assertEqual(Client.objects.count(), 2)
        self.assertEqual(Cart.objects.count(), 2)
        self.assertEqual(Product.objects.count(), 2)
        self.assertEqual(ProductInCart.objects.count(), 4)
        self.assertEqual(client.cart.products.count(), 2)
        self.assertEqual(client_copy.cart.products.count(), 2)

    def test_duplicate__multiple_level_nesting__non_abstract_inheritance(self):
        cart = PriorityCartFactory()
        client = ClientFactory(cart=cart)

        self.assertEqual(Client.objects.count(), 1)
        self.assertEqual(Cart.objects.count(), 1)
        self.assertEqual(PriorityCart.objects.count(), 1)

        client_copy = client.duplicate(paths=['cart.prioritycart'])

        self.assertEqual(Client.objects.count(), 2)
        self.assertEqual(Cart.objects.count(), 2)
        self.assertEqual(PriorityCart.objects.count(), 2)
        self.assertNotEqual(client_copy.cart.prioritycart, client.cart.prioritycart)


class MultiLevelOverrideFieldTestCase(TestCase):

    def setUp(self):
        self.book1 = BookFactory()
        self.book2 = BookFactory()
        self.library = LibraryFactory()  # type: Library
        self.library.books.add(self.book1)
        self.library.books.add(self.book2)
        self.building = BuildingFactory(library=self.library)  # type: Building
        self.building.previous_building = BuildingFactory(previous_building=self.building, library=None)
        self.building.save()
        self.library.nearest_building = self.building
        self.library.save()

    def test_override_simple_nested_value_and_simple_relation(self):
        overriden_name = 'Overriden building name'
        overriden_prevous_building = BuildingFactory()  # type: Building
        building_copy = self.building.duplicate(
            paths=['library.nearest_building', 'library.books', 'previous_building'],
            override_fields={
                'library.nearest_building.name': overriden_name,
                'previous_building': overriden_prevous_building,
            }
        )
        building_copy = Building.objects.get(pk=building_copy.pk)   # type: Building

        self.assertEqual(building_copy.library.nearest_building.name, overriden_name)
        self.assertEqual(building_copy.previous_building, overriden_prevous_building)

    def test_override_simple_value_nested_in_reverse_relation(self):
        self.library.building_set.add(*[BuildingFactory() for _ in range(2)])
        overriden_building_name = 'Overriden building name'
        library_copy = self.library.duplicate(
            paths=['building_set.*'],
            override_fields={
                'building_set.name': overriden_building_name,
            }
        )
        self.assertCountEqual(library_copy.building_set.values_list('name', flat=True), [overriden_building_name] * 3)

    def test_cannot_override_m2m_nested_relation(self):
        with self.assertRaises(NestedM2MOverride):
            self.building.duplicate(
                paths=['library.nearest_building', 'previous_building'],
                override_fields={
                    'library.books': [BookFactory(), BookFactory()],
                }
            )

    def test_override_value_with_callable(self):
        expected_nearest_building_name = self.building.library.nearest_building.name.lower()
        overriden_prevous_building = BuildingFactory()  # type: Building
        building_copy = self.building.duplicate(
            paths=['library.nearest_building', 'library.books', 'previous_building'],
            override_fields={
                'library.nearest_building.name': CallableValue(
                    lambda nearest_building: nearest_building.name.lower() if nearest_building.name else 'New name'
                ),
                'previous_building': CallableValue(lambda previous_building: overriden_prevous_building if True else None),
            }
        )
        building_copy = Building.objects.get(pk=building_copy.pk)   # type: Building

        self.assertEqual(building_copy.library.nearest_building.name, expected_nearest_building_name)
        self.assertEqual(building_copy.previous_building, overriden_prevous_building)

    def test_override_value_with_callable_that_returns_none(self):
        self.library.building_set.add(*[BuildingFactory() for _ in range(2)])
        library_copy = self.library.duplicate(
            paths=['building_set.*'],
            override_fields={
                'building_set.nullable': CallableValue(lambda building_set: None),
            }
        )
        self.assertCountEqual(library_copy.building_set.values_list('nullable', flat=True), [None] * 3)
