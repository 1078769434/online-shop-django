from django.db import models
from django.contrib.auth.models import AbstractBaseUser

from .managers import UserManager
from shop.models import Product


class User(AbstractBaseUser):
    """
    自定义用户模型，扩展自AbstractBaseUser，用于管理网站用户。

    属性:
    - email: 用户的电子邮箱地址，唯一字段。
    - full_name: 用户的全名。
    - is_admin: 标记是否为管理员。
    - is_active: 标记用户是否为激活状态。
    - likes: 用户喜欢的产品集合，可以为空。
    - is_manager: 标记是否为店铺经理，用于管理订单和产品。

    USERNAME_FIELD 和 REQUIRED_FIELDS 用于Django的用户认证系统。
    """

    email = models.EmailField(max_length=100, unique=True)
    full_name = models.CharField(max_length=100)
    is_admin = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    likes = models.ManyToManyField(Product, blank=True, related_name='likes')
    is_manager = models.BooleanField(default=False)

    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['full_name']

    def __str__(self):
        """
        返回用户模型的字符串表示形式，即邮箱地址。

        返回:
        - 用户的邮箱地址字符串。
        """
        return self.email

    def has_perm(self, perm, obj=None):
        """
        检查用户是否有特定权限。

        参数:
        - perm: 权限字符串。
        - obj: 目标对象，可选。

        返回:
        - 布尔值，始终为True，表示该用户具有所有权限。
        """
        return True

    def has_module_perms(self, app_label):
        """
        检查用户是否具有特定应用标签的所有权限。

        参数:
        - app_label: 应用标签字符串。

        返回:
        - 布尔值，始终为True，表示该用户具有所有应用的权限。
        """
        return True

    @property
    def is_staff(self):
        """
        判断用户是否为工作人员，即是否为管理员。

        返回:
        - 布尔值，如果is_admin为True，则返回True。
        """
        return self.is_admin

    def get_likes_count(self):
        """
        获取用户喜欢的产品数量。

        返回:
        - 喜欢的产品数量。
        """
        return self.likes.count()


class ShippingAddress(models.Model):
    """用户收货地址模型"""

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='shipping_addresses')
    name = models.CharField(max_length=50, verbose_name='收货人姓名')
    phone_number = models.CharField(max_length=16, verbose_name='联系电话')
    address_line1 = models.CharField(max_length=100, verbose_name='地址1')
    address_line2 = models.CharField(max_length=100, blank=True, verbose_name='地址2')
    city = models.CharField(max_length=50, verbose_name='城市')
    state_province = models.CharField(max_length=50, verbose_name='省/州')
    postal_code = models.CharField(max_length=20, verbose_name='邮政编码')
    default = models.BooleanField(default=False, verbose_name='设为默认')

    def __str__(self):
        return f"{self.name} - {self.address_line1}, {self.city}" 