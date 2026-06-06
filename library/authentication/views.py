from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from .models import CustomUser


def register_user(request):
    if request.method == "POST":
        email = request.POST.get("email")
        password = request.POST.get("password")
        first_name = request.POST.get("first_name")
        last_name = request.POST.get("last_name")
        middle_name = request.POST.get("middle_name")
        role = int(request.POST.get("role", 0))  # 0 - user, 1 - librarian

        if CustomUser.get_by_email(email) is None:
            user = CustomUser.create(
                email=email,
                password=password,
                first_name=first_name,
                last_name=last_name,
                middle_name=middle_name,
            )
            user.update(role=role)

            login(request, user, backend="django.contrib.auth.backends.ModelBackend")
            return redirect("user_list")
        else:
            return render(
                request,
                "authentication/register.html",
                {"error": "Користувач з таким email вже існує"},
            )

    return render(request, "authentication/register.html")


def login_user(request):
    if request.method == "POST":
        email = request.POST.get("email")
        password = request.POST.get("password")

        user = authenticate(request, email=email, password=password)

        if user is not None:
            login(request, user)
            return redirect("user_list")
        return render(
            request, "authentication/login.html", {"error": "Невірний email або пароль"}
        )

    return render(request, "authentication/login.html")


@login_required
def logout_user(request):
    if request.method == "POST":
        logout(request)
        return redirect("login_user")

    return redirect("user_list")


@login_required
def user_list(request):
    # Перевірка чи роль == 1 (librarian)
    if request.user.role != 1:
        return redirect("book_list")

    users = CustomUser.get_all()
    return render(request, "authentication/user_list.html", {"users": users})


@login_required
def user_detail(request, user_id):
    if request.user.role != 1:
        return render(request, "authentication/access_denied.html")

    target_user = CustomUser.get_by_id(user_id)
    if not target_user:
        return redirect("user_list")

    return render(
        request, "authentication/user_detail.html", {"target_user": target_user}
    )
