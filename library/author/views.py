from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import Author


@login_required
def author_list(request):
    if request.user.role != 1:
        return render(request, "authentication/access_denied.html")

    authors = Author.get_all()
    return render(request, "author/author_list.html", {"authors": authors})


@login_required
def author_create(request):
    if request.user.role != 1:
        return render(request, "authentication/access_denied.html")

    if request.method == "POST":
        name = request.POST.get("name")
        surname = request.POST.get("surname")
        patronymic = request.POST.get("patronymic")

        if name and surname:
            Author.create(name=name, surname=surname, patronymic=patronymic)
            return redirect("author_list")

    return render(request, "author/author_create.html")


@login_required
def author_delete(request, author_id):
    if request.user.role != 1 or request.method != "POST":
        return redirect("author_list")

    author = Author.get_by_id(author_id)

    if author:
        if not author.books.exists():
            Author.delete_by_id(author_id)

    return redirect("author_list")
