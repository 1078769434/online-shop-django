from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.decorators import user_passes_test
from django.http import Http404

from shop.models import Product
from accounts.models import User, ShippingAddress
from orders.models import Order, OrderItem
from .forms import AddProductForm, AddCategoryForm, EditProductForm

from accounts.forms import CustomUserCreationForm,CustomUserChangeForm
def is_manager(user):
    """
    检查用户是否为经理。

    参数:
    - user: 当前请求的用户对象。

    返回值:
    - 如果用户是经理，则返回 True；如果不是或用户信息不存在，则抛出 Http404 异常。
    """
    try:
        if not user.is_manager:
            raise Http404
        return True
    except:
        raise Http404

@user_passes_test(is_manager)
@login_required
def products(request):
    """
    显示所有产品的页面。

    参数:
    - request: HttpRequest 对象。

    返回值:
    - HttpResponse 对象，渲染的产品页面。
    """
    products = Product.objects.all()  # 获取所有产品
    context = {'title':'产品' ,'products':products}  # 页面上下文
    return render(request, 'products.html', context)  # 渲染页面

@user_passes_test(is_manager)
@login_required
def add_product(request):
    """
    添加产品的页面。

    参数:
    - request: HttpRequest 对象。

    返回值:
    - HttpResponse 对象，渲染的添加产品页面或重定向到产品列表。
    """
    if request.method == 'POST':  # 提交表单时
        form = AddProductForm(request.POST, request.FILES)  # 创建表单实例
        if form.is_valid():  # 表单验证通过
            form.save()  # 保存产品信息
            messages.success(request, 'Product added Successfuly!')  # 添加成功消息
            return redirect('dashboard:add_product')  # 重定向回添加产品页面
    else:  # 首次访问页面时
        form = AddProductForm()  # 创建空的表单实例
    context = {'title':'添加产品', 'form':form}  # 页面上下文
    return render(request, 'add_product.html', context)  # 渲染页面

@user_passes_test(is_manager)
@login_required
def delete_product(request, id):
    """
    删除指定产品的功能。

    参数:
    - request: HttpRequest 对象。
    - id: 要删除的产品的ID。

    返回值:
    - HttpResponse 对象，重定向到产品列表页面。
    """
    product = Product.objects.filter(id=id).delete()  # 根据ID删除产品
    messages.success(request, 'product has been deleted!', 'success')  # 添加删除成功消息
    return redirect('dashboard:products')  # 重定向到产品列表

@user_passes_test(is_manager)
@login_required
def edit_product(request, id):
    """
    编辑指定产品的页面。

    参数:
    - request: HttpRequest 对象。
    - id: 要编辑的产品的ID。

    返回值:
    - HttpResponse 对象，渲染的编辑产品页面或重定向到产品列表。
    """
    product = get_object_or_404(Product, id=id)  # 根据ID获取产品
    if request.method == 'POST':  # 提交表单时
        form = EditProductForm(request.POST, request.FILES, instance=product)  # 创建表单实例
        if form.is_valid():  # 表单验证通过
            form.save()  # 保存修改后的信息
            messages.success(request, 'Product has been updated', 'success')  # 添加更新成功消息
            return redirect('dashboard:products')  # 重定向到产品列表
    else:  # 首次访问页面时
        form = EditProductForm(instance=product)  # 创建表单实例
    context = {'title': '修改产品', 'form':form}  # 页面上下文
    return render(request, 'edit_product.html', context)  # 渲染页面

@user_passes_test(is_manager)
@login_required
def add_category(request):
    """
    添加类别的页面。

    参数:
    - request: HttpRequest 对象。

    返回值:
    - HttpResponse 对象，渲染的添加类别页面或重定向到类别列表。
    """
    if request.method == 'POST':  # 提交表单时
        form = AddCategoryForm(request.POST)  # 创建表单实例
        if form.is_valid():  # 表单验证通过
            form.save()  # 保存类别信息
            messages.success(request, 'Category added Successfuly!')  # 添加成功消息
            return redirect('dashboard:add_category')  # 重定向回添加类别页面
    else:  # 首次访问页面时
        form = AddCategoryForm()  # 创建空的表单实例
    context = {'title':'添加分类', 'form':form}  # 页面上下文
    return render(request, 'add_category.html', context)  # 渲染页面


# 确保只有经理能访问订单页面
@user_passes_test(is_manager)
@login_required
def orders(request):
    """
    显示所有订单的页面。

    参数:
    - request: HttpRequest对象，表示客户端请求的数据和相关信息。

    返回值:
    - HttpResponse对象，渲染的订单页面。
    """
    orders = Order.objects.all()  # 获取所有订单
    context = {'title':'订单', 'orders':orders}  # 准备上下文数据
    return render(request, 'orders.html', context)  # 渲染订单列表页面

# 确保只有经理能访问订单详情页面
@user_passes_test(is_manager)
@login_required
def order_detail(request, id):
    """
    显示特定订单的详细信息页面。

    参数:
    - request: HttpRequest对象，表示客户端请求的数据和相关信息。
    - id: 订单的唯一标识符。

    返回值:
    - HttpResponse对象，渲染的订单详情页面。
    """
    order = Order.objects.filter(id=id).first()  # 根据ID获取订单
    items = OrderItem.objects.filter(order=order).all()  # 获取该订单的所有商品
    # 获取订单所属用户的默认收货地址
    user = order.user
    addresses = ShippingAddress.objects.filter(user=user, default=True)

    # 准备上下文数据，新增addresses
    context = {
        'title': '订单详情',
        'items': items,
        'order': order,
        'addresses': addresses,  # 更新此行，传入与订单用户关联的地址
    }

    # 渲染并返回订单详情页面
    return render(request, 'order_detail.html', context)

@user_passes_test(is_manager)
@login_required
def users(request):
    """
    显示所有用户的页面。

    参数:
    - request: HttpRequest对象，表示客户端请求的数据和相关信息。

    返回值:
    - HttpResponse对象，渲染的用户管理页面。
    """
    users = User.objects.all()  # 获取所有用户
    context = {'title': '用户管理', 'users': users}  # 准备上下文数据
    return render(request, 'users.html', context)  # 渲染用户列表页面


@user_passes_test(is_manager)
@login_required
def add_user(request):
    """
    添加新用户的页面。

    参数:
    - request: HttpRequest对象，表示客户端请求的数据和相关信息。

    返回值:
    - HttpResponse对象，渲染的添加用户页面或重定向到用户列表。
    """
    if request.method == 'POST':  # 提交表单时
        form = CustomUserCreationForm(request.POST)  # 使用Django内置的UserCreationForm或其他自定义的用户创建表单
        if form.is_valid():  # 表单验证通过
            form.save()  # 保存新用户信息
            messages.success(request, 'User added successfully!')  # 添加成功消息
            return redirect('dashboard:users')  # 重定向到用户列表
    else:  # 首次访问页面时
        form = CustomUserCreationForm()  # 创建空的表单实例
    context = {'title': '添加用户', 'form': form}  # 页面上下文
    return render(request, 'add_user.html', context)  # 渲染添加用户页面


@user_passes_test(is_manager)
@login_required
def edit_user(request, user_id):
    """
    编辑用户信息的页面。

    参数:
    - request: HttpRequest对象，表示客户端请求的数据和相关信息。
    - user_id: 要编辑的用户的ID。

    返回值:
    - HttpResponse对象，渲染的编辑用户页面或重定向到用户列表。
    """
    user = get_object_or_404(User, pk=user_id)  # 根据ID获取用户
    if request.method == 'POST':  # 提交表单时
        form = CustomUserChangeForm(request.POST, instance=user)  # 使用Django内置的UserChangeForm或其他自定义的用户编辑表单
        if form.is_valid():  # 表单验证通过
            form.save()  # 保存修改后的用户信息
            messages.success(request, 'User information updated successfully!')  # 更新成功消息
            return redirect('dashboard:users')  # 重定向到用户列表
    else:  # 首次访问页面时
        form = CustomUserChangeForm(instance=user)  # 创建表单实例
    context = {'title': '修改用户信息', 'form': form}  # 页面上下文
    return render(request, 'edit_user.html', context)  # 渲染编辑用户页面


@user_passes_test(is_manager)
@login_required
def delete_user(request, user_id):
    """
    删除指定用户的功能。

    参数:
    - request: HttpRequest对象，表示客户端请求的数据和相关信息。
    - user_id: 要删除的用户的ID。

    返回值:
    - HttpResponse对象，重定向到用户列表页面。
    """
    user = get_object_or_404(User, pk=user_id)  # 根据ID获取用户
    user.delete()  # 删除用户
    messages.success(request, 'User has been deleted!', 'success')  # 添加删除成功消息
    return redirect('dashboard:users')  # 重定向到用户列表
