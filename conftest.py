import pytest
from pytest_factoryboy import register

from tests.factories import (AddressFactory, CategoryFactory, CustomerFactory,
                             ProductFactory, ProductSpecificationFactory,
                             ProductSpecificationValueFactory,
                             ProductTypeFactory,
                             OrderFactory,
                             OrderItemFactory)

register(CategoryFactory)
register(ProductTypeFactory)
register(ProductSpecificationFactory)
register(ProductSpecificationValueFactory)
register(ProductFactory)
register(CustomerFactory)
register(AddressFactory)
register(OrderFactory)
register(OrderItemFactory)

# Catalogue


@pytest.fixture
def product_category(db, category_factory):
    category = category_factory.create()
    return category


@pytest.fixture
def product_type(db, product_type_factory):
    product_type = product_type_factory.create()
    return product_type


@pytest.fixture
def product_spec(db, product_specification_factory):
    product_spec = product_specification_factory.create()
    return product_spec


@pytest.fixture
def product(db, product_factory):
    product = product_factory.create()
    return product


@pytest.fixture
def product_spec_value(db, product_secification_value_factory):
    product_spec_value = product_secification_value_factory.create()
    return product_spec_value


# Account
@pytest.fixture
def customer(db, customer_factory):
    new_customer = customer_factory.create()
    return new_customer


@pytest.fixture
def admin(db, customer_factory):
    new_customer = customer_factory.create(
        name="admin", is_staff=True, is_superuser=True
    )
    return new_customer


@pytest.fixture
def address(db, address_factory):
    new_address = address_factory.create()
    return new_address


@pytest.fixture
def order(db, order_factory):
    order = order_factory.create()
    return order


@pytest.fixture
def order_item(db, order_item_factory):
    order_item = order_item_factory.create()
    return order_item
