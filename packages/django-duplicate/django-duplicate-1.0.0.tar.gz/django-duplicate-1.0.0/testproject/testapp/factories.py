import factory


class AuthorFactory(factory.django.DjangoModelFactory):
    name = factory.Sequence(lambda n: 'Author %d' % n)
    professional = True

    class Meta:
        model = 'duplicate.Author'


class BookFactory(factory.django.DjangoModelFactory):
    title = factory.Sequence(lambda n: 'Book %d' % n)
    author = factory.SubFactory('testapp.factories.AuthorFactory')

    class Meta:
        model = 'duplicate.Book'


class LibraryFactory(factory.django.DjangoModelFactory):
    external_id = factory.Sequence(lambda n: n)

    class Meta:
        model = 'duplicate.Library'


class BuildingFactory(factory.django.DjangoModelFactory):
    name = factory.Sequence(lambda n: 'Building %d' % n)
    nullable = factory.Sequence(lambda n: 'Building nullable %d' % n)
    library = factory.SubFactory('testapp.factories.LibraryFactory')

    class Meta:
        model = 'duplicate.Building'


class DocumentFactory(factory.django.DjangoModelFactory):
    file = factory.django.FileField()

    class Meta:
        model = 'duplicate.Document'


class ParentFactory(factory.django.DjangoModelFactory):

    class Meta:
        model = 'duplicate.Parent'


class ChildFactory(factory.django.DjangoModelFactory):

    class Meta:
        model = 'duplicate.Child'


class ProductFactory(factory.django.DjangoModelFactory):
    name = factory.Sequence(lambda n: 'Product %d' % n)

    class Meta:
        model = 'duplicate.Product'


class CartFactory(factory.django.DjangoModelFactory):

    class Meta:
        model = 'duplicate.Cart'


class PriorityCartFactory(factory.django.DjangoModelFactory):

    class Meta:
        model = 'duplicate.PriorityCart'


class ClientFactory(factory.django.DjangoModelFactory):
    name = factory.Sequence(lambda n: 'Client %d' % n)
    cart = factory.SubFactory('testapp.factories.CartFactory')

    class Meta:
        model = 'duplicate.Client'


class ProductInCartFactory(factory.django.DjangoModelFactory):
    product = factory.SubFactory('testapp.factories.ProductFactory')
    cart = factory.SubFactory('testapp.factories.CartFactory')

    class Meta:
        model = 'duplicate.ProductInCart'
