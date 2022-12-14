from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path("admin/", admin.site.urls),
    path("basket/", include("ecommerce.apps.basket.urls", namespace="basket")),
    path("account/", include("ecommerce.apps.account.urls", namespace="account")),
    path("order/", include("ecommerce.apps.order.urls", namespace="order")),
    path("checkout/", include("ecommerce.apps.checkout.urls", namespace="checkout")),
    path("", include("ecommerce.apps.catalogue.urls", namespace="catalogue")),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
