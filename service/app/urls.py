from django.urls import path

from . import stripe_views, views

urlpatterns = [
    path("", views.HomePageView.as_view(), name="home"),
    path("buy/<int:pk>", stripe_views.create_checkout_session, name="buy"),
    path(
        "create-payment-intent/<int:pk>",
        stripe_views.create_payment_intent,
        name="create-payment-intent",
    ),
    path("success/", views.SuccessView.as_view()),
    path("item/<int:pk>", views.ItemView.as_view(), name="item"),
    path("items", views.ListItemsView.as_view(), name="list"),
    path("order", views.ListItemsOrderView.as_view(), name="order"),
    path("process-objects", views.process_objects, name="process_objects"),
    path("order_confirm", stripe_views.create_checkout_session_order, name="order_confirm"),
]
