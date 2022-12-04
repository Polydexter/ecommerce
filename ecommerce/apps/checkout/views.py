import json

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect, JsonResponse
from django.shortcuts import render
from django.urls import reverse
from paypalcheckoutsdk.orders import OrdersGetRequest

from ecommerce.apps.account.models import Address
from ecommerce.apps.basket.basket import Basket
from ecommerce.apps.order.models import Order, OrderItem

from .models import DeliveryOptions
from .paypal import PayPalClient


@login_required
def delivery_options(request):
    deliveryoptions = DeliveryOptions.objects.filter(is_active=True)
    return render(
        request, "checkout/delivery_options.html", {"options": deliveryoptions}
    )


@login_required
def basket_update_delivery(request):
    basket = Basket(request)
    if request.POST.get("action") == "post":
        delivery_option = int(request.POST.get("delivery_option"))
        delivery_type = DeliveryOptions.objects.get(id=delivery_option)

        session = request.session
        if "delivery" not in request.session:
            session["delivery"] = {
                "delivery_id": delivery_type.id,
            }
        else:
            session["delivery"]["delivery_id"] = delivery_type.id
            session.modified = True

        delivery_price = delivery_type.delivery_price
        updated_total_price = basket.get_total_price()

        return JsonResponse(
            {
                "total": updated_total_price,
                "delivery_price": delivery_price,
            }
        )


@login_required
def delivery_address(request):
    session = request.session
    if "delivery" not in request.session:
        messages.success(request, "Please select delivery option")
        return HttpResponseRedirect(request.META["HTTP_REFERER"])

    addresses = Address.objects.filter(customer=request.user).order_by("-default")
    if len(addresses) == 0:
        messages.success(request, "You do not have any addresses yet")
        return HttpResponseRedirect(reverse("account:addresses"))

    if "address" not in request.session:
        session["address"] = {"address_id": str(addresses[0].id)}
    else:
        session["address"]["address_id"] = str(addresses[0].id)
        session.modified = True

    return render(request, "checkout/delivery_address.html", {"addresses": addresses})


@login_required
def payment_selection(request):
    session = request.session
    if "address" not in session:
        messages.success(request, "Please select address option")
        return HttpResponseRedirect(request.META["HTTP_REFERER"])

    return render(request, "checkout/payment_selection.html", {})


@login_required
def payment_complete(request):
    PPClient = PayPalClient()

    body = json.loads(request.body)
    data = body["orderID"]
    user_id = request.user.id

    requestorder = OrdersGetRequest(data)
    response = PPClient.client.execute(requestorder)

    total_paid = response.result.purchase_units[0].amount.value

    basket = Basket(request)
    order = Order.objects.create(
        user_id=user_id,
        full_name=response.result.purchase_units[0].shipping.name.full_name,
        email=response.result.payer.email_address,
        address1=response.result.purchase_units[0].shipping.address.address_line_1,
        address2=response.result.purchase_units[0].shipping.address.admin_area_2,
        postal_code=response.result.purchase_units[0].shipping.address.postal_code,
        country_code=response.result.purchase_units[0].shipping.address.country_code,
        total_paid=total_paid,
        order_key=response.result.id,
        payment_option="paypal",
        billing_status=True,
    )
    order_id = order.pk

    for item in basket:
        OrderItem.objects.create(
            order_id=order_id,
            product=item["product"],
            price=item["price"],
            quantity=item["quantity"],
        )

    return JsonResponse("Payment completed!", safe=False)


@login_required
def payment_success(request):
    basket = Basket(request)
    basket.clear()
    return render(request, "checkout/payment_successful.html", {})
