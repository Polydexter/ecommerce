import pytest

def test_order_str(order):
    assert order.__str__() == str(order.created)


def test_order_item_str(order_item):
    assert order_item.__str__() == str(order_item.id)