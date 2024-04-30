from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout

from .forms import UserRegistrationForm, UserLoginForm, ManagerLoginForm, EditProfileForm, ShippingAddressForm
from accounts.models import User, ShippingAddress


def create_manager():
    """
    系统启动时执行一次的功能：
    此函数将在online_shop/urls.py中调用。
    检查是否存在邮箱为manager@example.com的用户，如果不存在，则创建一个具有管理员角色的用户。
    """
    if not User.objects.filter(email="manager@example.com").first():
        user = User.objects.create_user(
            "manager@example.com", 'shop manager', 'managerpass1234'
        )
        # 为该用户设置管理员角色
        user.is_manager = True
        user.save()


def manager_login(request):
    """
    管理员登录功能。

    参数:
    - request: HTTP请求对象。

    返回值:
    - 重定向到管理员仪表盘页面或登录页面。
    """
    if request.method == 'POST':
        form = ManagerLoginForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            user = authenticate(
                request, email=data['email'], password=data['password']
            )
            if user is not None and user.is_manager:
                login(request, user)
                return redirect('dashboard:products')
            else:
                messages.error(
                    request, 'username or password is wrong', 'danger'
                )
                return redirect('accounts:manager_login')
    else:
        form = ManagerLoginForm()
    context = {'form': form}
    return render(request, 'manager_login.html', context)


def user_register(request):
    """
    用户注册功能。

    参数:
    - request: HTTP请求对象。

    返回值:
    - 重定向到用户登录页面或注册页面。
    """
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            user = User.objects.create_user(
                data['email'], data['full_name'], data['password']
            )
            return redirect('accounts:user_login')
    else:
        form = UserRegistrationForm()
    context = {'title': 'Signup', 'form': form}
    return render(request, 'register.html', context)


def user_login(request):
    """
    用户登录功能。

    参数:
    - request: HTTP请求对象。

    返回值:
    - 重定向到商店首页或用户登录页面。
    """
    if request.method == 'POST':
        form = UserLoginForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            user = authenticate(
                request, email=data['email'], password=data['password']
            )
            if user is not None:
                login(request, user)
                return redirect('shop:home_page')
            else:
                messages.error(
                    request, 'username or password is wrong', 'danger'
                )
                return redirect('accounts:user_login')
    else:
        form = UserLoginForm()
    context = {'title': 'Login', 'form': form}
    return render(request, 'login.html', context)


def user_logout(request):
    """
    用户登出功能。

    参数:
    - request: HTTP请求对象。

    返回值:
    - 重定向到用户登录页面。
    """
    logout(request)
    return redirect('accounts:user_login')


def edit_profile(request):
    """
    编辑用户个人资料功能。

    参数:
    - request: HTTP请求对象。

    返回值:
    - 渲染编辑个人资料页面或重定向到编辑个人资料页面。
    """
    form = EditProfileForm(request.POST, instance=request.user)
    if form.is_valid():
        form.save()
        messages.success(request, 'Your profile has been updated', 'success')
        return redirect('accounts:edit_profile')
    else:
        form = EditProfileForm(instance=request.user)
    context = {'title': 'Edit Profile', 'form': form}
    return render(request, 'edit_profile.html', context)


def manage_shipping_address(request):
    """
    用户管理收货地址功能。

    参数:
    - request: HTTP请求对象。

    返回值:
    - 渲染收货地址管理页面或执行添加、编辑、删除等操作后重定向至收货地址管理页面。
    """


    # 添加地址操作
    if request.method == 'POST' and 'add_address' in request.POST:
        form = ShippingAddressForm(request.POST)
        if form.is_valid():
            address = form.save(commit=False)
            address.user = request.user
            address.save()
            messages.success(request, '新收货地址已添加成功.', 'success')
            return redirect('accounts:manage_shipping_address')

    # 编辑地址操作
    elif request.method == 'POST' and 'edit_address' in request.POST:
        # form = ShippingAddressForm(request.POST, instance=request.POST.get('address_id'))
        address_id = request.POST.get('address_id')
        address_instance = ShippingAddress.objects.get(id=address_id)  # 假设ShippingAddress是你的模型类
        form = ShippingAddressForm(request.POST, instance=address_instance)
        if form.is_valid():
            form.save()
            messages.success(request, '收货地址已更新.', 'success')
            return redirect('accounts:manage_shipping_address')

    # 删除地址操作
    elif request.method == 'POST' and 'delete_address' in request.POST:
        # address_id = request.POST.get('address_id')
        address_id = request.POST.get('address_id')
        # address_instance = ShippingAddress.objects.get(id=address_id)  # 假设ShippingAddress是你的模型类
        # form = ShippingAddressForm(request.POST, instance=address_instance)
        ShippingAddress.objects.filter(id=address_id, user=request.user).delete()
        messages.success(request, '收货地址已删除.', 'success')
        return redirect('accounts:manage_shipping_address')

    # 列出用户所有收货地址
    addresses = ShippingAddress.objects.filter(user=request.user)
    form = ShippingAddressForm()
    # 渲染管理页面
    context = {'addresses': addresses, 'title': '收货地址', 'form': form}
    return render(request, 'manage_shipping_address.html', context)

# def add_shipping_address(request):
#     """
#     用户添加收货地址功能。
#
#     参数:
#     - request: HTTP请求对象。
#
#     返回值:
#     - 添加成功：渲染收货地址管理页面并显示成功消息，然后重定向至收货地址管理页面。
#     """
#     if request.method == 'POST':
#         form = ShippingAddressForm(request.POST)
#         if form.is_valid():
#             address = form.save(commit=False)
#             address.user = request.user
#             address.save()
#             messages.success(request, '新收货地址已添加成功.', 'success')
#             return redirect('accounts:manage_shipping_address')
#     else:
#         form = ShippingAddressForm()
#
#     return render(request, 'add_shipping_address_template.html', {'form': form})
#
#
# def edit_shipping_address(request, address_id):
#     """
#     用户编辑收货地址功能。
#
#     参数:
#     - request: HTTP请求对象。
#     - address_id: 要编辑的收货地址ID。
#
#     返回值:
#     - 编辑成功：渲染收货地址管理页面并显示成功消息，然后重定向至收货地址管理页面。
#     """
#     address = get_object_or_404(ShippingAddress, id=address_id, user=request.user)
#
#     if request.method == 'POST':
#         form = ShippingAddressForm(request.POST, instance=address)
#         if form.is_valid():
#             form.save()
#             messages.success(request, '收货地址已更新.', 'success')
#             return redirect('accounts:manage_shipping_address')
#     else:
#         form = ShippingAddressForm(instance=address)
#
#     return render(request, 'edit_shipping_address_template.html', {'form': form})
#
# def delete_shipping_address(request, address_id):
#     """
#     用户删除收货地址功能。
#
#     参数:
#     - request: HTTP请求对象。
#     - address_id: 要删除的收货地址ID。
#
#     返回值:
#     - 删除成功：显示成功消息，然后重定向至收货地址管理页面。
#     """
#     address = get_object_or_404(ShippingAddress, id=address_id, user=request.user)
#     address.delete()
#     messages.success(request, '收货地址已删除.', 'success')
#     return redirect('accounts:manage_shipping_address')