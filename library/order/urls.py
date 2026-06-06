from django.urls import path
from . import views

urlpatterns = [
    path("list/", views.order_list, name="order_list"),
    path("create/<int:book_id>/", views.order_create, name="order_create"),
    path("close/<int:order_id>/", views.order_close, name="order_close"),
]
