import factory
from faker import Faker

from ecommerce.apps.account.models import Address, Customer
from ecommerce.apps.catalogue.models import (Category, Product,
                                             ProductSpecification,
                                             ProductSpecificationValue,
                                             ProductType)
from ecommerce.apps.order.models import Order, OrderItem

fake = Faker()

###
# Catalogue
###


class CategoryFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Category
        django_get_or_create = ("name", "slug")

    name = "django"
    slug = "django"


class ProductTypeFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = ProductType
        django_get_or_create = ("name",)

    name = "book"


class ProductSpecificationFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = ProductSpecification

    product_type = factory.SubFactory(ProductTypeFactory)
    name = "pages"


class ProductFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Product

    product_type = factory.SubFactory(ProductTypeFactory)
    category = factory.SubFactory(CategoryFactory)
    title = "product_title"
    description = fake.text()
    slug = "product_slug"
    regular_price = "9.99"
    discount_price = "4.99"


class ProductSpecificationValueFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = ProductSpecificationValue

    product = factory.SubFactory(ProductFactory)
    specification = factory.SubFactory(ProductSpecificationFactory)
    value = "100"


###
# Account
###


class CustomerFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Customer

    email = "test@example.com"
    name = "test_user"
    mobile = "+987654321"
    password = "test_secret"
    is_active = True
    is_staff = False

    @classmethod
    def _create(cls, model_class, *args, **kwargs):
        manager = cls._get_manager(model_class)
        if "is_superuser" in kwargs:
            return manager.create_superuser(*args, **kwargs)
        else:
            return manager.create_user(*args, **kwargs)


class AddressFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Address

    customer = factory.SubFactory(CustomerFactory)
    full_name = fake.name()
    phone = fake.phone_number()
    postcode = fake.postcode()
    address_line = fake.street_address()
    address_line2 = fake.street_address()
    town_city = fake.city_suffix()
    country = fake.country()

###
# Order
###

class OrderFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Order
    
    user = factory.SubFactory(CustomerFactory)
    full_name = fake.name()
    address1 = fake.street_address()
    address2 = fake.street_address()
    city = fake.city_suffix()
    phone = fake.phone_number()
    postal_code = fake.postcode()
    total_paid = fake.pydecimal(left_digits=3, right_digits=2)
    order_key = "order_key"
    payment_option = "payment_option"
    billing_status = True


class OrderItemFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = OrderItem

    order = factory.SubFactory(OrderFactory)
    product = factory.SubFactory(ProductFactory)
    price = fake.pydecimal(left_digits=3, right_digits=2)
    quantity = 1