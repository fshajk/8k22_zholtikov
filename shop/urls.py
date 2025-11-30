from django.urls import path
from .views import *
from django.contrib.auth.views import LogoutView


urlpatterns = [
    path('', CatalogView.as_view(), name='catalog'),
    path('accounts/profile/', CatalogView.as_view(), name='catalog'),
    path('catalog', CatalogView.as_view(), name='catalog'),
    path('search_catalog', SearchCatalogView.as_view(), name='search_catalog'),
    path('logout/', LogoutView.as_view(next_page='/'), name='logout'),
    path('products/<int:pk>', ProductDetailView.as_view(), name='product_detail'),
    path('cart', view_cart, name='cart'),
    path('add_to_cart/<int:product_id>', add_to_cart, name='add_to_cart'),
    path('sub_to_cart/<int:product_id>', sub_to_cart, name='sub_to_cart'),
    path('orders', OrdersListView.as_view(), name='orders'),
    path('order_detail/<int:pk>', OrderDetailView.as_view(), name='order_detail'),
    path('submit_order', submit_order, name='submit_order'),
    path('create_order', create_order, name='create_order'),
]
