from datetime import datetime

from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.http import Http404
from django.shortcuts import render, redirect
from django.utils.decorators import method_decorator
from django.views.generic import ListView, DetailView

from shop.models import Product, OrderItem
from .models import CartItem, Order


class CatalogView(ListView):
    template_name = "catalog.html"
    model = Product
    context_object_name = "list_of_all_products"


class SearchCatalogView(ListView):
    template_name = "catalog.html"
    model = Product
    context_object_name = "list_of_all_products"

    def get_queryset(self):
        query = self.request.GET.get('q')
        if query:  # Проверяйте, есть ли запрос
            return Product.objects.filter(
                Q(name__icontains=query) | Q(description__icontains=query)
            )
        else:
            return Product.objects.all()


class ProductDetailView(DetailView):
    template_name = "product_detail.html"
    model = Product
    context_object_name = "product"


def view_cart(request):
    cart_items = []
    total_cost = 0
    if request.user.is_authenticated:
        cart_items = CartItem.objects.filter(user=request.user)
        total_cost = sum(item.product.price * item.quantity for item in cart_items)
    return render(
        request, 'cart.html',
        context={"cart_items": cart_items, "total_cost": total_cost}
    )


def add_to_cart(request, product_id):
    if request.user.is_authenticated:
        cart_item, created = CartItem.objects.get_or_create(user=request.user, product_id=product_id)
        if not created:
            cart_item.quantity += 1
        cart_item.cost = cart_item.product.price * cart_item.quantity
        cart_item.save()
    return redirect('cart')


def sub_to_cart(request, product_id):
    if request.user.is_authenticated:
        cart_item = CartItem.objects.get(user=request.user, product_id=product_id)
        cart_item.quantity -= 1
        cart_item.cost = cart_item.product.price * cart_item.quantity
        if cart_item.quantity <= 0:
            cart_item.delete()
        else:
            cart_item.save()
    return redirect('cart')


@method_decorator(login_required, name='dispatch')
class OrdersListView(ListView):
    template_name = "order/orders.html"
    model = Order
    context_object_name = "list_of_all_orders"

    def get_queryset(self):
        # Возвращаем только заказы текущего пользователя
        return Order.objects.filter(user=self.request.user)


@method_decorator(login_required, name='dispatch')
class OrderDetailView(DetailView):
    template_name = "order/order_detail.html"
    model = Order
    context_object_name = "order"

    def get_queryset(self):
        # Ограничиваем доступ: пользователь видит только свои заказы
        return Order.objects.filter(user=self.request.user)

    def get(self, request, *args, **kwargs):
        # Дополнительно проверяем, что объект существует и принадлежит пользователю
        try:
            self.object = self.get_object()
        except Http404:
            # Если заказ не найден или не принадлежит пользователю — редирект или ошибка
            return redirect('orders_list')  # или вернуть 403/404
        context = self.get_context_data(object=self.object)
        return self.render_to_response(context)


def submit_order(request):
    if request.user.is_authenticated:
        cart_items = CartItem.objects.filter(user=request.user)
        total_cost = sum(item.product.price * item.quantity for item in cart_items)
        if not cart_items:
            return redirect('cart')
        return render(
            request, 'order/submit_order.html',
            context={"cart_items": cart_items, "total_cost": total_cost,
                     "today": datetime.today().strftime("%Y-%m-%d")}
        )
    return redirect('login')


def create_order(request):
    if request.user.is_authenticated:
        cart_items = CartItem.objects.filter(user=request.user)
        if not cart_items:
            return redirect('cart')
        order = Order.objects.create(
            user=request.user,
            order_date=request.POST.get('order_date'),
            address=request.POST.get('address', 'pickup'),
            price=sum(item.product.price * item.quantity for item in cart_items)
        )
        order.save()
        for cart_item in cart_items:
            order_item = OrderItem.objects.create(
                order=order,
                product=cart_item.product,
                price=cart_item.cost,
                quantity=cart_item.quantity
            )
            order_item.save()
            cart_item.delete()
        return redirect(f'order_detail/{order.order_id}')
    return redirect('login')
