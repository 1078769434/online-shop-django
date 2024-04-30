from django.db import models

from accounts.models import User
from shop.models import Product


class Order(models.Model):
    """
    订单模型，代表一个用户的订单

    属性:
        user: 关联的用户模型，使用外键连接到User模型
        created: 订单创建时间，自动设置为当前时间
        updated: 订单最后更新时间，每次保存模型时自动设置为当前时间
        status: 订单状态，默认为False（未支付）
    """

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='orders')  # 用户外键
    created = models.DateTimeField(auto_now_add=True)  # 创建时间
    updated = models.DateTimeField(auto_now=True)  # 更新时间
    status = models.BooleanField(default=False)  # 订单状态

    class Meta:
        ordering = ('-created',)  # 默认按照创建时间降序排序

    def __str__(self):
        """
        返回订单的字符串表示形式

        返回:
            字符串: 格式为"用户全名 - 订单id: 订单编号"
        """
        return f"{self.user.full_name} - order id: {self.id}"

    @property
    def get_total_price(self):
        """
        计算订单的总价格

        返回:
            订单的总价格（整数）
        """
        total = sum(item.get_cost() for item in self.items.all())  # 累加所有订单项的成本
        return total

class OrderItem(models.Model):
    """
    订单项模型，代表订单中的一个商品

    属性:
        order: 关联的订单模型，使用外键连接到Order模型
        product: 关联的产品模型，使用外键连接到Product模型
        price: 商品单价（整数）
        quantity: 商品数量（小整数，默认为1）
    """

    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='items')  # 订单外键
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='order_items')  # 产品外键
    price = models.IntegerField()  # 单价
    quantity = models.SmallIntegerField(default=1)  # 数量

    def __str__(self):
        """
        返回订单项的字符串表示形式

        返回:
            订单项的id（字符串形式）
        """
        return str(self.id)

    def get_cost(self):
        """
        计算订单项的成本

        返回:
            订单项的成本（整数），即单价乘以数量
        """
        return self.price * self.quantity
