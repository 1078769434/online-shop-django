from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage

from shop.models import Product, Category
from cart.forms import QuantityForm


def paginat(request, list_objects):
    """
    对象分页函数。

    参数:
    - request: HttpRequest对象，用于获取用户请求信息。
    - list_objects: 需要进行分页的对象列表。

    返回:
    - 返回一个分页后的对象页面。
    """
    p = Paginator(list_objects, 20)  # 使用Paginator类将列表对象分页，每页包含20个对象
    page_number = request.GET.get('page')  # 从请求中获取用户请求的页面编号
    try:
        page_obj = p.get_page(page_number)  # 尝试根据页面编号获取对应的页面对象
    except PageNotAnInteger:
        # 如果页面编号不是整数，则返回第1页
        page_obj = p.page(1)
    except EmptyPage:
        # 如果请求的页面超出范围，则返回最后一页
        page_obj = p.page(p.num_pages)
    return page_obj


def home_page(request):
    """
    首页渲染函数。

    参数:
    - request: HttpRequest对象，用于获取用户请求信息。

    返回:
    - 返回首页的HttpResponse对象。
    """
    products = Product.objects.all()  # 获取所有产品对象
    context = {'products': paginat(request ,products)}  # 将分页后的产品传递给上下文
    return render(request, 'home_page.html', context)  # 渲染并返回首页模板


def product_detail(request, slug):
    """
    显示产品的详细信息页面。

    参数:
    - request: HttpRequest对象，表示客户端请求的数据和相关信息。
    - slug: 字符串，产品的唯一标识符，用于从URL中获取特定产品。

    返回值:
    - HttpResponse对象，渲染的产品详细信息页面。
    """
    form = QuantityForm()  # 初始化数量表单
    product = get_object_or_404(Product, slug=slug)  # 根据slug获取产品对象，如果不存在则返回404错误页面
    related_products = Product.objects.filter(category=product.category).all()[:5]  # 获取与该产品相同类别的其他5个产品
    context = {
        'title': product.title,  # 产品标题
        'product': product,  # 产品对象
        'form': form,  # 数量表单
        'favorites': 'favorites',  # 用于标识收藏状态的初始值
        'related_products': related_products  # 相关产品列表
    }
    # 检查当前用户是否已将该产品添加为收藏
    if request.user.likes.filter(id=product.id).first():
        context['favorites'] = 'remove'
    return render(request, 'product_detail.html', context)


@login_required
def add_to_favorites(request, product_id):
    """
    将产品添加到用户的收藏列表中。

    参数:
    - request: HttpRequest对象，表示客户端请求的数据和相关信息。
    - product_id: 整数，要添加到收藏列表的产品的ID。

    返回值:
    - HttpResponseRedirect对象，重定向到产品的详细信息页面。
    """
    product = get_object_or_404(Product, id=product_id)  # 根据产品ID获取产品对象
    request.user.likes.add(product)  # 将产品添加到用户的收藏列表
    return redirect('shop:product_detail', slug=product.slug)  # 重定向到产品的详细信息页面



# 必须登录才能从收藏中移除商品
@login_required
def remove_from_favorites(request, product_id):
    # 根据商品ID获取商品对象，如果不存在则返回404
    product = get_object_or_404(Product, id=product_id)
    # 从当前用户的喜欢列表中移除该商品
    request.user.likes.remove(product)
    # 移除成功后重定向到收藏页面
    return redirect('shop:favorites')

# 必须登录才能查看收藏列表
@login_required
def favorites(request):
    # 获取当前用户喜欢的所有商品
    products = request.user.likes.all()
    # 渲染收藏页面，传递标题和商品列表
    context = {'title':'Favorites', 'products':products}
    return render(request, 'favorites.html', context)

# 实现商品搜索功能
def search(request):
    # 从请求的GET参数中获取查询字符串
    query = request.GET.get('q')
    # 根据查询字符串搜索商品，并获取所有匹配结果
    products = Product.objects.filter(title__icontains=query).all()
    # 对搜索结果进行分页，并传递到首页进行渲染
    context = {'products': paginat(request ,products)}
    return render(request, 'home_page.html', context)

# 根据分类筛选商品
def filter_by_category(request, slug):
    """
    当用户点击父分类时，我们希望显示其所有子分类中的所有商品。
    """
    # 根据slug获取分类对象，如果不存在则返回空列表
    result = []
    category = Category.objects.filter(slug=slug).first()
    # 将属于该分类的所有商品添加到结果列表中
    [result.append(product) \
        for product in Product.objects.filter(category=category.id).all()]
    # 如果该分类是父分类，则获取所有子分类，并将其商品也添加到结果中
    if not category.is_sub:
        sub_categories = category.sub_categories.all()
        # 遍历子分类，将子分类中的所有商品添加到结果列表中
        for category in sub_categories:
            [result.append(product) \
                for product in Product.objects.filter(category=category).all()]
    # 对筛选结果进行分页，并传递到首页进行渲染
    context = {'products': paginat(request ,result)}
    return render(request, 'home_page.html', context)

