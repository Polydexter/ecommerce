from django.http import JsonResponse
from django.shortcuts import get_object_or_404, render

from ecommerce.apps.catalogue.models import Product

from .basket import Basket


def basket_summary(request):
    basket = Basket(request)
    return render(request, "basket/summary.html", {"basket": basket})


def basket_add(request):
    basket = Basket(request)
    if request.POST.get("action") == "post":
        product_id = int(request.POST.get("productid"))
        product_qty = int(request.POST.get("productqty"))
        product = get_object_or_404(Product, id=product_id)
        basket.add(product=product, quantity=product_qty)
        total_qty = basket.__len__()
        subtotal = basket.get_total_price()
        response = JsonResponse({"qty": total_qty, "subtotal": subtotal})
        return response


def basket_delete(request):
    basket = Basket(request)
    if request.POST.get("action") == "post":
        product_id = request.POST.get("productid")
        basket.delete(product=product_id)
        subtotal = str(basket.get_subtotal_price())
        total = str(basket.get_total_price())
        items_qty = str(len(basket))
        response = JsonResponse(
            {
                "Success": True,
                "subtotal": subtotal,
                "total": total,
                "items_qty": items_qty,
            }
        )
        return response


def basket_update(request):
    basket = Basket(request)
    if request.POST.get("action") == "post":
        product_id = request.POST.get("productid")
        product_qty = request.POST.get("productqty")
        basket.update(product=product_id, qty=product_qty)
        total = str(basket.get_total_price())
        items_qty = str(len(basket))
        subtotal = str(basket.get_subtotal_price())
        response = JsonResponse(
            {
                "Success": True,
                "subtotal": subtotal,
                "items_qty": items_qty,
                "total": total,
            }
        )
        return response
