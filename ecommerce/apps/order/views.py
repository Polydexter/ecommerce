from django.contrib.auth.decorators import login_required
from django.http.response import JsonResponse
from django.shortcuts import render

from ecommerce.apps.basket.basket import Basket

from .models import Order, OrderItem


def add(request):
    basket = Basket(request)
    if request.POST.get("action") == "post":
        user_id = request.user.id
        order_key = request.POST.get("order_key")
        basket_total = basket.get_total_price()

        # Chel if ther order exists
        if Order.objects.filter(order_key=order_key).exists():
            pass
        else:
            order = Order.objects.create(
                user_id=user_id,
                full_name="name",
                address1="add1",
                address2="add2",
                total_paid=basket_total,
                order_key=order_key,
            )
            order_id = order.pk
            for item in basket:
                OrderItem.objects.create(
                    order_id=order_id,
                    product=item["product"],
                    price=item["price"],
                    quantity=item["quantity"],
                )
            response = JsonResponse({"success": "Return something"})
        return response


@login_required
def user_orders(request):
    user_id = request.user.id
    orders = Order.objects.filter(user_id=user_id).filter(billing_status=True)
    return render(request, "account/dashboard/user_orders.html", {"orders": orders})
