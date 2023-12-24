import json

import stripe
from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.http.response import JsonResponse
from django.shortcuts import redirect
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_GET

from .models import Item, Order, Price

stripe.api_key = settings.STRIPE_SECRET_KEY


@require_GET
def create_checkout_session(request, pk):
    domain_url = settings.DOMAIN
    try:
        cancel_url = domain_url + f"item/{pk}"
        item = Item.objects.get(pk=pk)
        product = item.prices.filter(currency=item.currency).first()

        checkout_session = stripe.checkout.Session.create(
            success_url=domain_url +
            "success?session_id={CHECKOUT_SESSION_ID}",
            cancel_url=cancel_url,
            payment_method_types=["card"],
            mode="payment",
            line_items=[
                {
                    "price": product.stripe_price_id,
                    "quantity": 1,
                }],
        )

        return JsonResponse({"sessionId": checkout_session["id"]})
    except Exception as e:
        print(e)
        return JsonResponse({"error": str(e)})

@require_GET
@login_required
def create_checkout_session_order(request):
    domain_url = settings.DOMAIN
    
    try:
        cancel_url = domain_url + f"order"
        prices = Price.objects.filter(
            product__orders__order__user_id=request.user, currency="USD"
        )
        order = Order.objects.filter(user=request.user)
        if order.exists():
            order = order.first()
            if order.tax:
                tax = order.tax.stripe_tax_id

            line_items = [
                {
                    "price": i.stripe_price_id,
                    "quantity": 1,
                    "tax_rates": [tax] if order.tax else [],
                }
                for i in prices
            ]
        else:
            return redirect('order')
        checkout_session = stripe.checkout.Session.create(
            success_url=domain_url + "success?session_id={CHECKOUT_SESSION_ID}",
            cancel_url=cancel_url,
            payment_method_types=["card"],
            mode="payment",
            line_items=line_items,
            discounts=[{"promotion_code": order.discount.stripe_discount_id}]
            if order.discount
            else [],
        )

        return JsonResponse({"sessionId": checkout_session["id"]})
    except Exception as e:
        print(e)
        return JsonResponse({"error": str(e)})


def create_payment_intent(request, pk):
    try:
        req_json = json.loads(request.body)
        customer = stripe.Customer.create(email=req_json["email"])
        product = Item.objects.get(pk=pk)
        price = product.prices.filter(currency=product.currency)
        price = price.first().price if price.exists() else product.price
        intent = stripe.PaymentIntent.create(
            amount=int(price * 100),
            currency=product.currency,
            customer=customer["id"],
            metadata={"product_id": product.id},
        )
        return JsonResponse({"clientSecret": intent["client_secret"]})
    except Exception as e:
        print(e)
        return (JsonResponse(error=str(e)),)


@csrf_exempt
def stripe_webhook(request):
    endpoint_secret = settings.STRIPE_ENDPOINT_SECRET
    payload = request.body
    sig_header = request.META["HTTP_STRIPE_SIGNATURE"]
    event = None
    try:
        event = stripe.Webhook.construct_event(
            payload, sig_header, endpoint_secret)
    except ValueError as e:
        return HttpResponse(status=400)
    except stripe.error.SignatureVerificationError as e:
        return HttpResponse(status=400)

    if event["type"] == "checkout.session.completed":
        print("Payment was successful.")

    return HttpResponse(status=200)
