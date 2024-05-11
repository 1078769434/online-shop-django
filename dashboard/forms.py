from django import forms
from django.forms import ModelForm

from shop.models import Product, Category

from django.utils.translation import gettext as _
class AddProductForm(ModelForm):
    """
    用于添加产品的表单类，继承自ModelForm。

    Meta:
        model: 指定表单关联的模型是Product。
        fields: 定义表单包含的字段，即产品信息的编辑字段。
    """
    class Meta:
        model = Product
        fields = ['category', 'image', 'title','description', 'price']

    def __init__(self, *args, **kwargs):
        """
        构造函数，初始化表单实例。

        参数:
            *args: 位置参数。
            **kwargs: 关键字参数。
        """
        super(AddProductForm, self).__init__(*args, **kwargs)
        # 设置字段的中文标签
        self.fields['category'].label = _("类别")
        self.fields['image'].label = _("图片")
        self.fields['title'].label = _("标题")
        self.fields['description'].label = _("描述")
        self.fields['price'].label = _("价格")

        # 为所有可见字段的控件添加 'form-control' 类
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control'


class AddCategoryForm(ModelForm):
    """
    用于添加类别的表单类，继承自ModelForm。

    Meta:
        model: 指定表单关联的模型是Category。
        fields: 定义表单包含的字段，即类别信息的编辑字段。
    """
    class Meta:
        model = Category
        fields = ['title', 'sub_category','is_sub']

    def __init__(self, *args, **kwargs):
        """
        构造函数，初始化表单实例。

        参数:
            *args: 位置参数。
            **kwargs: 关键字参数。
        """
        super(AddCategoryForm, self).__init__(*args, **kwargs)

        # 设置字段的中文标签
        self.fields['title'].label = _("类别名称")
        self.fields['sub_category'].label = _("子类别")
        self.fields['is_sub'].label = _("是否为子类别")

        # 为特定字段的控件添加自定义类
        self.fields['is_sub'].widget.attrs['class'] = 'form-check-input'
        self.fields['sub_category'].widget.attrs['class'] = 'form-control'
        self.fields['title'].widget.attrs['class'] = 'form-control'
        # self.fields['slug'].widget.attrs['class'] = 'form-control'


class EditProductForm(ModelForm):
    """
    用于编辑产品的表单类，继承自ModelForm。

    Meta:
        model: 指定表单关联的模型是Product。
        fields: 定义表单包含的字段，即产品信息的编辑字段。
    """
    class Meta:
        model = Product
        fields = ['category', 'image', 'title','description', 'price']

    def __init__(self, *args, **kwargs):
        """
        构造函数，初始化表单实例。

        参数:
            *args: 位置参数。
            **kwargs: 关键字参数。
        """
        super(EditProductForm, self).__init__(*args, **kwargs)

        # 设置字段的中文标签
        self.fields['category'].label = _("类别")
        self.fields['image'].label = _("图片")
        self.fields['title'].label = _("标题")
        self.fields['description'].label = _("描述")
        self.fields['price'].label = _("价格")

        # 为所有可见字段的控件添加 'form-control' 类
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control'


