from django.db import models
from django.urls import reverse
from django.template.defaultfilters import slugify


class Category(models.Model):
    """
    类别模型，用于表示商品的类别信息。

    属性:
    - title: 类别名称，字符串类型。
    - sub_category: 子类别，外键连接到Category模型自身，允许为空。
    - is_sub: 是否为子类别，布尔类型，默认为False。
    - slug: 类别名称的slug化版本，用于URL，唯一。
    """

    title = models.CharField(max_length=200)
    sub_category = models.ForeignKey(
        'self', on_delete=models.CASCADE,
        related_name='sub_categories', null=True, blank=True
    )
    is_sub = models.BooleanField(default=False)
    """
    这个 slug 字段类型是 Django ORM 中的一个内置字段类型，
    名为 SlugField。SlugField 主要用来存储简短的、可读性强且通常用于 URL 的标识符，
    它通常由小写字母、数字、下划线组成，并且不包含空格或其他特殊字符。
    这种类型的字段常用于创建简洁、友好的网址（URL）或者在数据库中作为唯一且具有语义意义的标识。
    """
    slug = models.SlugField(max_length=200, unique=True)

    def __str__(self):
        """
        返回类别的名称字符串。

        返回值:
        - 类别的名称。
        """
        return self.title

    def get_absolute_url(self):
        """
        获取类别的绝对URL。

        返回值:
        - 类别详细页面的URL。
        """
        return reverse('shop:product_detail', kwargs={'slug':self.slug})

    def save(self, *args, **kwargs):
        """
        重写save方法，以自动slug化标题。

        参数:
        - *args: 变参，未使用。
        - **kwargs: 变参字典，未使用。

        返回值:
        - 调用父类save方法的返回值。
        """
        self.slug = slugify(self.title)
        return super().save(*args, **kwargs)


class Product(models.Model):
    """
    产品模型，用于表示商品信息。

    属性:
    - category: 商品类别，外键连接到Category模型。
    - image: 商品图片，图像字段。
    - title: 商品标题，字符串类型。
    - description: 商品描述，文本字段。
    - price: 商品价格，整型。
    - date_created: 创建日期，日期时间字段，自动添加。
    - slug: 商品标题的slug化版本，用于URL，唯一。
    """

    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='category')
    image = models.ImageField(upload_to='products')
    title = models.CharField(max_length=250)
    description = models.TextField()
    price = models.IntegerField()
    date_created = models.DateTimeField(auto_now_add=True)
    slug = models.SlugField(unique=True)

    class Meta:
        """
        Meta类用于定义模型的元数据选项。

        属性:
        - ordering: 模型对象的默认排序方式，按照创建日期降序排列。
        """
        ordering = ('-date_created',)

    def __str__(self):
        """
        返回商品的slug作为字符串表示。

        返回值:
        - 商品的slug。
        """
        return self.slug

    def get_absolute_url(self):
        """
        获取商品的绝对URL。

        返回值:
        - 商品详细页面的URL。
        """
        return reverse('shop:product_detail', kwargs={'slug':self.slug})

    def save(self, *args, **kwargs):
        """
        重写save方法，以自动slug化标题。

        参数:
        - *args: 变参，未使用。
        - **kwargs: 变参字典，未使用。

        返回值:
        - 调用父类save方法的返回值。
        """
        self.slug = slugify(self.title)
        return super().save(*args, **kwargs)
