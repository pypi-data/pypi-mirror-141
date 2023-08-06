from django.db import models

from duplicate.models import DuplicateMixin


class Author(DuplicateMixin, models.Model):
    name = models.CharField(max_length=100)
    professional = models.BooleanField(default=False)

    class Meta:
        app_label = 'duplicate'


class Book(DuplicateMixin, models.Model):
    title = models.CharField(max_length=100)
    author = models.ForeignKey(Author, on_delete=models.CASCADE)

    class Meta:
        app_label = 'duplicate'


class Library(DuplicateMixin, models.Model):
    external_id = models.AutoField(primary_key=True)
    books = models.ManyToManyField(Book)
    nearest_building = models.ForeignKey('Building', null=True, related_name='nearest_libraries', on_delete=models.PROTECT)

    class Meta:
        app_label = 'duplicate'


class Building(DuplicateMixin, models.Model):
    library = models.ForeignKey(Library, null=True, on_delete=models.CASCADE)
    previous_building = models.ForeignKey("self", null=True, on_delete=models.CASCADE)
    name = models.CharField(max_length=50)
    nullable = models.CharField(max_length=50, blank=True, null=True)

    class Meta:
        app_label = 'duplicate'


class Document(DuplicateMixin, models.Model):
    file = models.FileField()

    class Meta:
        app_label = 'duplicate'


class Child(models.Model):

    class Meta:
        app_label = 'duplicate'


class Parent(DuplicateMixin, models.Model):
    children = models.ManyToManyField(
        Child,
        through='duplicate.ChildForParent'
    )

    class Meta:
        app_label = 'duplicate'


class ChildForParent(models.Model):
    child = models.ForeignKey(Child, on_delete=models.PROTECT)
    parent = models.ForeignKey(Parent, related_name='+', on_delete=models.CASCADE)

    class Meta:
        app_label = 'duplicate'
        unique_together = ('child', 'parent')


class Product(models.Model):
    name = models.CharField(max_length=100)

    class Meta:
        app_label = 'duplicate'


class Cart(models.Model):
    products = models.ManyToManyField(Product, through='duplicate.ProductInCart')

    class Meta:
        app_label = 'duplicate'


class PriorityCart(Cart):
    class Meta:
        app_label = 'duplicate'


class Client(DuplicateMixin, models.Model):
    name = models.CharField(max_length=100)
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE)

    class Meta:
        app_label = 'duplicate'


class ProductInCart(models.Model):
    product = models.ForeignKey(Product, on_delete=models.PROTECT)
    cart = models.ForeignKey(Cart, related_name='+', on_delete=models.CASCADE)

    class Meta:
        app_label = 'duplicate'
