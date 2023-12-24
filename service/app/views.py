from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
import stripe
from typing import Any
from django.http.response import JsonResponse
from django.views.generic.base import TemplateView
from django.views.generic import DetailView, ListView
from .models import Item, Price, Order, Order_of_items, Discount, Tax
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import ObjectDoesNotExist


class HomePageView(TemplateView):
    template_name = "home.html"


class SuccessView(TemplateView):
    template_name = "success.html"


class ItemView(DetailView):
    model = Item
    template_name = "item.html"

    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        item = self.get_object()
        product = item.prices.filter(currency=item.currency).first()
        context["price"] = product.price
        context["currency"] = product.currency
        return context


class ListItemsAbstract(ListView):
    model = Item

    class Meta:
        abstract = True


class ListItemsView(ListItemsAbstract):
    template_name = "list.html"



class ListItemsOrderView(LoginRequiredMixin, ListItemsAbstract):
    template_name = "order.html"

    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        user = self.request.user
        items_in_order = Item.objects.filter(orders__order__user=user).prefetch_related('orders__order').distinct()
        context['items_in_order'] = items_in_order
        try:
            orders = user.orders
        except (ObjectDoesNotExist, Exception):
            orders = False

        if orders:
            context['discount'] = orders.discount
            context['tax'] = orders.tax

        return context



@require_POST
@login_required
def process_objects(request):
    object_id = request.POST.get("object_id", None)
    is_checked = request.POST.get("is_checked", None)
    user = request.user

    print(request.POST["object_id"], request.POST["is_checked"])
    if object_id is None or is_checked is None:
        return JsonResponse({"message": "Ошибка"}, status=400)

    is_checked = True if is_checked == "true" else False
    order, _ = Order.objects.get_or_create(user=user)
    try:
        object_id = int(object_id)
        if is_checked:
            Order_of_items.objects.get_or_create(
                item_id=object_id, order=order)
        else:
            Order_of_items.objects.filter(
                item_id=object_id, order=order).delete()
    except ValueError:
        if object_id == "FRIENDS20":
            discount = Discount.objects.get(name="FRIENDS20")
            order.discount = discount if is_checked else None
        else:
            tax = Tax.objects.get(name="GST")
            order.tax = tax if is_checked else None
        order.save()
        order.refresh_from_db()

    finally:
        return JsonResponse(
            {"message": "Объекты успешно обработаны!"}, status=200)
