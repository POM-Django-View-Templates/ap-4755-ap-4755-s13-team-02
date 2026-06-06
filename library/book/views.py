from django.shortcuts import render, redirect, get_object_or_404
from .models import Book
from author.models import Author
from authentication.models import CustomUser
from order.models import Order


def book_list(request):
    books = Book.objects.all()
    title = request.GET.get("title")
    author = request.GET.get("author")
    if title:
        books = books.filter(name__icontains=title)
    if author:
        books = books.filter(authors__surname__icontains=author)
    return render(request, "book/book_list.html", {"books": books})


def book_detail(request, book_id):
    book = get_object_or_404(Book, id=book_id)
    return render(request, "book/book_detail.html", {"book": book})


def book_create(request):
    if request.user.role != 1:
        return redirect("book_list")
    if request.method == "POST":
        book = Book.create(
            name=request.POST.get("name"),
            description=request.POST.get("description"),
            count=request.POST.get("count"),
        )
        author_ids = request.POST.getlist("authors")
        if book and author_ids:
            book.authors.set(Author.objects.filter(id__in=author_ids))
        return redirect("book_list")
    return render(request, "book/book_create.html", {"authors": Author.get_all()})


def user_books(request, user_id):
    if request.user.role != 1:
        return redirect("book_list")
    user = get_object_or_404(CustomUser, id=user_id)
    orders = Order.objects.filter(user=user, end_at__isnull=True)
    return render(request, "book/user_books.html", {"user": user, "orders": orders})
