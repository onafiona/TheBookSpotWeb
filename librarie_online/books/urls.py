from django.urls import path
from . import views

app_name='books'
urlpatterns=[
    path("", views.BooksListView.as_view(), name="book_list"),
    path("<int:pk>/", views.BooksDetailView.as_view(), name="book_detail"),
    path('add_to_cart/<int:book_id>/', views.add_to_cart, name='add_to_cart'),
    path('cart/', views.view_cart, name='view_cart'),
    path('cart/change_quantity/<int:book_id>/', views.change_quantity, name='change_quantity'),
    path('cart/clear/', views.clear_cart, name='clear_cart'),
]