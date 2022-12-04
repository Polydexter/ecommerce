import pytest

from ecommerce.apps.account.forms import RegistrationForm, UserAddressForm
from ecommerce.apps.account.models import Customer


@pytest.mark.parametrize(
    "full_name, phone, address_line, address_line2, town_city, postcode, validity",
    [
        ("mike", "23456789", "addr1", "addr2", "town", "code", True),
        ("", "4567890", "addr1", "addr2", "town", "code", False),
    ],
)
def test_address_form(
    full_name, phone, address_line, address_line2, town_city, postcode, validity
):
    form = UserAddressForm(
        data={
            "full_name": full_name,
            "phone": phone,
            "address_line": address_line,
            "address_line2": address_line2,
            "town_city": town_city,
            "postcode": postcode,
        }
    )
    assert form.is_valid() is validity


def test_address_add(client, customer):
    user = customer
    client.force_login(user)
    client.post(
        "/account/address_add/",
        data={
            "full_name": "Name",
            "phone": "12345678",
            "address_line": "addr1",
            "address_line2": "addr2",
            "town_city": "town",
            "postcode": "code",
        },
    )
    assert len(user.user_addresses.all()) == 1


def test_address_add_no_input(client, customer):
    user = customer
    client.force_login(user)
    client.post(
        "/account/address_add/",
        data={
            "full_name": "",
            "phone": "",
            "address_line": "",
            "address_line2": "",
            "town_city": "",
            "postcode": "",
        },
    )
    assert len(user.user_addresses.all()) == 0


@pytest.mark.parametrize(
    "name, email, password, password2, validity",
    [
        ("user1", "a@a.com", "12345a", "12345a", True),
        ("user1", "a@a.com", "12345a", "", False),  # no second password
        ("user1", "a@a.com", "12345a", "12345b", False),  # password mismatch
        ("user1", "a@.com", "12345a", "12345a", False),  # email
    ],
)
@pytest.mark.django_db
def test_account_create(name, email, password, password2, validity):
    form = RegistrationForm(
        data={
            "name": name,
            "email": email,
            "password": password,
            "password2": password2,
        },
    )
    assert form.is_valid() is validity


@pytest.mark.parametrize(
    "name, email, password, password2, validity",
    [
        ("user1", "a@a.com", "12345a", "12345a", 1),
        ("user1", "a@a.com", "12345a", "12345", 0),
        ("user1", "", "12345a", "12345", 0),
    ],
)
@pytest.mark.django_db
def test_account_create_output(client, name, email, password, password2, validity):
    response = client.post(
        "/account/register/",
        data={
            "name": name,
            "email": email,
            "password": password,
            "password2": password2,
        },
    )
    assert len(Customer.objects.all()) == validity
