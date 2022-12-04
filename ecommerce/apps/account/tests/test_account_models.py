import pytest


def test_customer_str(customer):
    assert customer.__str__() == "test_user"


def test_superuser_str(admin):
    assert admin.__str__() == "admin"


def test_customer_email_no_input(customer_factory):
    with pytest.raises(ValueError) as e:
        customer_factory.create(email="")
    assert str(e.value) == "Customer Account: You must provide an email address"


def test_customer_email_invalid_input(customer_factory):
    with pytest.raises(ValueError) as e:
        customer_factory.create(email="test@test")
    assert str(e.value) == "You must provide a valid email address"


def test_admin_email_no_input(customer_factory):
    with pytest.raises(ValueError) as e:
        customer_factory.create(email="", is_staff=True, is_superuser=True)
    assert str(e.value) == "Admin Account: You must provide an email address"


def test_admin_is_staff_false(customer_factory):
    with pytest.raises(ValueError) as e:
        customer_factory.create(email="", is_staff=False, is_superuser=True)
    assert str(e.value) == "Superuser must be assigned to is_staff=True."


def test_admin_is_superuser_false(customer_factory):
    with pytest.raises(ValueError) as e:
        customer_factory.create(email="", is_staff=True, is_superuser=False)
    assert str(e.value) == "Superuser must be assigned to is_superuser=True."


def test_address_str(address):
    assert address.__str__() == "{} Address".format(address.full_name)
