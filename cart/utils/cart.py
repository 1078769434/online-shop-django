from shop.models import Product

# 购物车会话ID
CART_SESSION_ID = 'cart'

class Cart:
    """
    购物车类，用于管理用户购物车中的商品。

    参数:
    - request: HttpRequest对象，用于访问用户的会话。

    属性:
    - session: HttpRequest对象中的会话，用于存储购物车信息。
    - cart: 字典，存储购物车中的商品及其数量。
    """
    def __init__(self, request):
        """
        初始化购物车实例。

        参数:
        - request: HttpRequest对象。
        """
        self.session = request.session
        self.cart = self.add_cart_session()

    def __iter__(self):
        """
        迭代购物车中的每个商品，附加商品实例和总价。

        返回:
        - 生成器，包含每个商品的信息。
        """
        product_ids = self.cart.keys()
        products = Product.objects.filter(id__in=product_ids)
        cart = self.cart.copy()
        for product in products:
            cart[str(product.id)]['product'] = product
        for item in cart.values():
            item['total_price'] = int(item['price']) * int(item['quantity'])
            yield item

    def add_cart_session(self):
        """
        创建或获取购物车会话。

        返回:
        - 购物车会话字典。
        """
        cart = self.session.get(CART_SESSION_ID)
        if not cart:
            cart = self.session[CART_SESSION_ID] = {}
        return cart

    def add(self, product, quantity):
        """
        将商品添加到购物车。

        参数:
        - product: Product实例，要添加的商品。
        - quantity: 整数，添加的商品数量。
        """
        product_id = str(product.id)

        if product_id not in self.cart:
            self.cart[product_id] = {'quantity': 0, 'price': str(product.price)}

        self.cart.get(product_id)['quantity'] += quantity
        self.save()

    def remove(self, product):
        """
        从购物车中移除商品。

        参数:
        - product: Product实例，要移除的商品。
        """
        product_id = str(product.id)
        if product_id in self.cart:
            del self.cart[product_id]
            self.save()

    def save(self):
        """
        保存购物车会话的修改。
        """
        self.session.modified = True

    def get_total_price(self):
        """
        计算购物车中所有商品的总价。

        返回:
        - 整数，购物车中所有商品的总价。
        """
        return sum(int(item['price']) * item['quantity'] for item in self.cart.values())

    def clear(self):
        """
        清除购物车中的所有商品。
        """
        del self.session[CART_SESSION_ID]
        self.save()
