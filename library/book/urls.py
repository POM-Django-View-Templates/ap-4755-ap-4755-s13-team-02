from django.urls import path
from . import views

urlpatterns = [
    path("list/", views.book_list, name="book_list"),
    path("detail/<int:book_id>/", views.book_detail, name="book_detail"),
    path("create/", views.book_create, name="book_create"),
    path("user/<int:user_id>/", views.user_books, name="user_books"),
]
