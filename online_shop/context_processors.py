# 从购物车工具包导入Cart类
from cart.utils.cart import Cart
# 从商店模型导入Category类
from shop.models import Category

def return_cart(request):
    """
    获取并返回当前用户的购物车中的项目数量。

    参数:
    - request: HttpRequest对象，表示客户端的HTTP请求。

    返回值:
    - 一个字典，包含购物车中的项目数量。
    """
    # 获取购物车中项目的数量
    cart = len(list(Cart(request)))
    return {'cart_count': cart}

def return_categories(request):
    """
    获取并返回网站中的所有商品分类。

    参数:
    - request: HttpRequest对象，表示客户端的HTTP请求。

    返回值:
    - 一个字典，包含所有的商品分类。
    """
    # 获取所有分类
    categories = Category.objects.all()
    return {'categories': categories}
