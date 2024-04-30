from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required

from cart.utils.cart import Cart
from .forms import QuantityForm
from shop.models import Product


"""

@login_required 是 Django 框架提供的一个装饰器，它用于保护视图函数或类视图，确保只有已登录的用户才能访问被装饰的视图。
当一个视图函数前加上 @login_required 后，如果未经过身份验证（即用户未登录）的用户尝试访问该视图时，
Django 会自动重定向用户到预先配置好的登录页面。
通常这个行为是通过检查 request.user 是否是已认证的用户来实现的，如果用户未登录，则 request.user 将是一个匿名用户实例。


"""

@login_required  # 要求用户登录后才能执行该函数
def add_to_cart(request, product_id):
    """
    将指定产品添加到购物车中。

    参数:
    - request: HttpRequest对象，表示客户端的HTTP请求。
    - product_id: 整型，指定要添加到购物车中的产品的ID。

    返回值:
    - HttpResponseRedirect对象，重定向到产品详情页面。
    """
    cart = Cart(request)  # 根据请求创建或获取购物车对象
    product = get_object_or_404(Product, id=product_id)  # 根据产品ID获取产品对象，如果不存在则返回404错误页面
    form = QuantityForm(request.POST)  # 使用请求中的POST数据初始化数量表单
    if form.is_valid():  # 检查表单数据是否有效
        data = form.cleaned_data  # 获取清理后的表单数据
        cart.add(product=product, quantity=data['quantity'])  # 将产品添加到购物车中，指定数量
        messages.success(request, 'Added to your cart!', 'info')  # 向用户显示成功消息
    return redirect('shop:product_detail', slug=product.slug)  # 重定向回产品详情页面


@login_required  # 要求用户登录后才能访问购物车页面
def show_cart(request):
    """
    显示用户的购物车页面。

    参数:
    - request: HttpRequest对象，表示客户端请求的数据和相关信息。

    返回值:
    - HttpResponse对象，渲染的购物车页面。
    """
    cart = Cart(request)  # 根据用户请求创建或获取购物车对象
    context = {'title': 'Cart', 'cart': cart}  # 准备传递给模板的上下文数据
    return render(request, 'cart.html', context)  # 渲染购物车页面并返回给客户端



@login_required
def remove_from_cart(request, product_id):
    """
    从购物车中移除指定产品。

    参数：
    - request: HTTP请求对象，用于获取当前用户的购物车信息。
    - product_id: 要移除的产品ID。

    返回值：
    - 重定向到购物车页面的响应对象。
    """
    # 获取当前用户的购物车
    cart = Cart(request)
    # 根据产品ID获取产品对象，如果不存在则返回404页面
    product = get_object_or_404(Product, id=product_id)
    # 从购物车中移除指定产品
    cart.remove(product)
    # 重定向到购物车页面
    return redirect('cart:show_cart')
