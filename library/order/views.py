import datetime
from django.shortcuts import render, redirect, get_object_or_404
from django.utils import timezone
from .models import Order
from book.models import Book


def order_list(request):
    orders = (
        Order.objects.all()
        if request.user.role == 1
        else Order.objects.filter(user=request.user)
    )
    return render(request, "order/order_list.html", {"orders": orders})


def order_create(request, book_id):
    if request.user.role == 1:
        return redirect("order_list")
    book = get_object_or_404(Book, id=book_id)
    if request.method == "POST":
        plated_dt = datetime.datetime.strptime(
            request.POST.get("plated_end_at"), "%Y-%m-%d"
        )
        Order.create(user=request.user, book=book, plated_end_at=plated_dt)
        return redirect("order_list")
    return render(request, "order/order_create.html", {"book": book})


def order_close(request, order_id):
    if request.user.role == 1 and request.method == "POST":
        order = get_object_or_404(Order, id=order_id)
        order.update(end_at=timezone.now())
    return redirect("order_list")
