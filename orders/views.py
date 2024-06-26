from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required

from django.views.decorators.http import require_POST, require_GET
from django.utils import timezone

from accounts.forms import ShippingAddressForm
from accounts.models import ShippingAddress
from shop.models import Product
from .models import Order, OrderItem
from cart.utils.cart import Cart


@login_required
def create_order(request):
    """
    创建订单视图函数。
    使用用户的购物车信息创建订单，并将购物车中的项目添加到订单中。

    参数:
    - request: HttpRequest对象，包含客户端发来的HTTP请求信息。

    返回值:
    - HttpResponseRedirect对象，重定向到订单支付页面。
    """
    cart = Cart(request)  # 获取用户的购物车
    order = Order.objects.create(user=request.user)  # 为用户创建一个新的订单
    for item in cart:  # 遍历购物车中的每一项
        OrderItem.objects.create(
            order=order, product=item['product'],
            price=item['price'], quantity=item['quantity']
        )
    return redirect('orders:pay_order', order_id=order.id)  # 重定向到支付页面


@login_required
def checkout(request, order_id):
    """
    结账视图函数。
    显示订单的结算信息。

    参数:
    - request: HttpRequest对象。
    - order_id: 订单的ID，用于获取特定的订单信息。

    返回值:
    - HttpResponse对象，渲染的结账页面。
    """
    order = get_object_or_404(Order, id=order_id)  # 根据订单ID获取订单对象
    context = {'title': 'Checkout', 'order': order}  # 准备上下文数据
    return render(request, 'checkout.html', context)  # 渲染结账页面


@login_required
def fake_payment(request, order_id):
    """
    模拟支付视图函数。
    模拟支付过程，清除购物车中的项目，并将订单状态标记为已支付。

    参数:
    - request: HttpRequest对象。
    - order_id: 订单的ID，用于获取特定的订单信息。

    返回值:
    - HttpResponseRedirect对象，重定向到用户订单页面。
    """
    cart = Cart(request)  # 获取用户的购物车
    cart.clear()  # 清除购物车中的所有项目
    order = get_object_or_404(Order, id=order_id)  # 根据订单ID获取订单对象
    order.status = True  # 将订单状态设置为已支付
    order.save()  # 保存订单状态的更新
    return redirect('orders:user_orders')  # 重定向到用户订单列表

@login_required
def direct_checkout(request, product_id):
    """
    直接购买视图函数。
    允许用户直接购买一个商品，无需将其添加到购物车。

    参数:
    - request: HttpRequest对象。
    - product_id: 商品的ID，用于获取特定的商品信息。

    返回值:
    - 如果商品存在并且用户已登录，重定向到订单支付页面。
    - 如果商品不存在，返回错误页面或提示信息。
    """
    product = get_object_or_404(Product, id=product_id)  # 根据商品ID获取商品对象
    order = Order.objects.create(user=request.user)  # 为用户创建一个新的订单
    OrderItem.objects.create(
        order=order, product=product,
        price=product.price, quantity=1  # 数量默认为1
    )
    # 模拟支付过程：直接将订单状态改为已支付
    order.status = True
    order.save()
    return redirect('orders:user_orders')  # 重定向到用户订单列表

@login_required
def user_orders(request):
    """
    用户订单视图函数。
    显示用户的所有订单列表。

    参数:
    - request: HttpRequest对象。

    返回值:
    - HttpResponse对象，渲染的用户订单列表页面。
    """
    # 列出用户所有收货地址
    addresses = ShippingAddress.objects.filter(user=request.user, default=True)
    form = ShippingAddressForm()

    orders = request.user.orders.all()  # 获取当前用户的所有订单
    context = {'title': 'Orders', 'orders': orders, 'addresses': addresses}  # 准备上下文数据
    return render(request, 'user_orders.html', context)  # 渲染用户订单列表页面



