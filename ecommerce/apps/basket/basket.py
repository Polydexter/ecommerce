from decimal import Decimal

from django.conf import settings

from ecommerce.apps.catalogue.models import Product
from ecommerce.apps.checkout.models import DeliveryOptions


class Basket:
    """
    A base Basket class, providing some default behaviors
    that can be inherited or overridden, as necessary.
    """

    def __init__(self, request):
        self.session = request.session
        basket = self.session.get(settings.BASKET_SESSION_ID)
        if settings.BASKET_SESSION_ID not in request.session:
            basket = self.session[settings.BASKET_SESSION_ID] = {}
        self.basket = basket

    def add(self, product, quantity):
        """
        Adding and updating the users basket session data
        """
        product_id = str(product.id)
        if product_id not in self.basket.keys():
            self.basket[product_id] = {
                "price": str(product.regular_price),
                "quantity": int(quantity),
            }
        else:
            total_single_qty = int(self.basket[product_id]["quantity"]) + int(quantity)
            self.basket[product_id] = {
                "price": str(product.regular_price),
                "quantity": total_single_qty,
            }
        self.save()

    def update(self, product, qty):
        """
        Updating single item quantity in the session data
        """
        if product in self.basket:
            self.basket[product]["quantity"] = int(qty)
            self.save()

    def delete(self, product):
        """
        Delete item from session data
        """
        product_id = product
        if product_id in self.basket:
            del self.basket[product_id]
            self.save()

    def save(self):
        self.session.modified = True

    def __iter__(self):
        """
        Collect the product_id in the session data to query
        the database and return products
        """
        product_ids = self.basket.keys()
        products = Product.objects.filter(id__in=product_ids)
        basket = self.basket.copy()

        for product in products:
            basket[str(product.id)]["product"] = product

        for item in basket.values():
            item["price"] = Decimal(item["price"])
            item["total_price"] = item["price"] * item["quantity"]
            yield item

    def __len__(self):
        """
        Get the basket data and count the qty of items
        """
        return sum(item["quantity"] for item in self.basket.values())

    def get_subtotal_price(self):
        return sum(
            Decimal(item["price"]) * int(item["quantity"])
            for item in self.basket.values()
        )

    def get_delivery_price(self):
        if "delivery" in self.session:
            price = DeliveryOptions.objects.get(
                pk=self.session["delivery"]["delivery_id"]
            ).delivery_price
            return price
        else:
            return Decimal(0.00)

    def get_total_price(self):
        subtotal = sum(
            Decimal(item["price"]) * int(item["quantity"])
            for item in self.basket.values()
        )
        delivery_price = Decimal(0.00)
        if "delivery" in self.session:
            delivery_price = DeliveryOptions.objects.get(
                pk=self.session["delivery"]["delivery_id"]
            ).delivery_price

        if subtotal == 0:
            shipping = Decimal(0.00)
        else:
            shipping = Decimal(delivery_price)

        total = subtotal + shipping
        return total

    def clear(self):
        del self.session[settings.BASKET_SESSION_ID]
        del self.session["address"]
        del self.session["delivery"]
        self.save()
