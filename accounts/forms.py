from django import forms

from .models import User, ShippingAddress

from django.contrib.auth.forms import UserCreationForm, UserChangeForm

from django.utils.translation import gettext as _

#
# 用户登录表单
#
class UserLoginForm(forms.Form):
    """
    用户登录表单

    字段说明:
    - email: 电子邮件字段，使用EmailInput作为输入小部件，附加样式和占位符。
    - password: 密码字段，使用PasswordInput作为输入小部件，附加样式和占位符。
    """
    email = forms.EmailField(
        widget=forms.EmailInput(
            attrs={'class': 'form-control', 'placeholder': 'email'}
        )
    )
    password = forms.CharField(
        widget=forms.PasswordInput(
            attrs={'class': 'form-control', 'placeholder': 'password'}
        )
    )

class UserRegistrationForm(forms.Form):
    """
    用户注册表单

    字段说明:
    - email: 电子邮件字段，使用EmailInput作为输入小部件，附加样式和占位符。
    - full_name: 全名字段，使用TextInput作为输入小部件，附加样式和占位符。
    - password: 密码字段，使用PasswordInput作为输入小部件，附加样式和占位符。
    """
    email = forms.EmailField(
        widget=forms.EmailInput(
            attrs={'class': 'form-control', 'placeholder': 'email'}
        )
    )
    full_name = forms.CharField(
        widget=forms.TextInput(
            attrs={'class': 'form-control', 'placeholder': 'full name'}
        )
    )
    password = forms.CharField(
        widget=forms.PasswordInput(
            attrs={'class': 'form-control', 'placeholder': 'password'}
        )
    )

#
# 管理员登录表单
#
class ManagerLoginForm(forms.Form):
    """
    管理员登录表单

    字段说明:
    - email: 电子邮件字段，使用EmailInput作为输入小部件，附加样式和占位符。
    - password: 密码字段，使用PasswordInput作为输入小部件，附加样式和占位符。
    """
    email = forms.EmailField(
        widget=forms.EmailInput(
            attrs={'class': 'form-control', 'placeholder': 'email'}
        )
    )
    password = forms.CharField(
        widget=forms.PasswordInput(
            attrs={'class': 'form-control', 'placeholder': 'password'}
        )
    )


#
# 编辑个人资料表单
# 使用ModelForm关联到User模型，只编辑'full_name'和'email'字段
#
class EditProfileForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['full_name', 'email']





class ShippingAddressForm(forms.ModelForm):
    """收货地址表单"""

    class Meta:
        model = ShippingAddress
        fields = ['name', 'phone_number', 'address_line1', 'address_line2', 'city', 'state_province', 'postal_code', 'default']
        widgets = {
            'name': forms.TextInput(attrs={'placeholder': '收货人姓名'}),
            'phone_number': forms.TextInput(attrs={'placeholder': '联系电话'}),
            'address_line1': forms.TextInput(attrs={'placeholder': '街道地址1'}),
            'address_line2': forms.TextInput(attrs={'placeholder': '街道地址2（可选）'}),
            'city': forms.TextInput(attrs={'placeholder': '城市'}),
            'state_province': forms.TextInput(attrs={'placeholder': '省/州'}),
            'postal_code': forms.TextInput(attrs={'placeholder': '邮政编码'}),
        }

    def clean(self):
        cleaned_data = super().clean()
        # 这里可以添加自定义的表单验证逻辑，如检查电话号码格式、邮编有效性等





class CustomUserCreationForm(forms.ModelForm):
    """
    一个定制的用户创建表单，继承自ModelForm。

    属性:
        Meta: 内嵌类，用于指定表单使用的模型和字段。
        is_active: 表单字段，用于指定用户是否激活。
        is_manager: 表单字段，用于指定用户是否为经理。

    方法:
        __init__(self, *args, **kwargs): 构造函数，初始化表单字段属性。
        save(self, commit=True): 保存表单数据至模型实例。
    """

    class Meta:
        """
        表单元数据的元信息，指定了表单关联的模型和字段。
        """
        model = User  # 指定表单关联的模型是User。
        fields = ['full_name', 'email', 'password', 'is_active', 'is_manager']  # 指定表单包含的字段。

    def __init__(self, *args, **kwargs):
        """
        构造函数，初始化表单。

        参数:
            *args: 位置参数。
            **kwargs: 关键字参数。
        """
        super().__init__(*args, **kwargs)
        # 为指定字段更新HTML属性，例如添加class和placeholder。
        self.fields['full_name'].widget.attrs.update({'class': 'form-control', 'placeholder': _('请输入昵称')})
        self.fields['email'].widget.attrs.update({'class': 'form-control', 'placeholder': _('请输入电子邮件')})
        self.fields['password'].widget.attrs.update({'class': 'form-control', 'placeholder': _('请输入密码')})
        # 此处注释的代码块用于更新is_active和is_manager字段的HTML属性。
        # 更改特定字段的标签
        self.fields['full_name'].label = _('昵称')
        self.fields['email'].label = _('电子邮件')
        self.fields['password'].label = _('密码')
        self.fields['is_active'].label = _('是否活跃')
        self.fields['is_manager'].label = _('是否为管理员')
    def save(self, commit=True):
        """
        保存表单数据至模型实例。

        参数:
            commit: 布尔值，默认为True，指定是否提交至数据库。

        返回值:
            无返回值。
        """
        user = super().save(commit=False)
        # 此处可添加自定义逻辑，例如在创建用户时设置额外属性或关联其他模型。
        if commit:
            user.save()
        return
    # 覆盖is_active和is_manager字段，将其设置为BooleanField，并定义标签。
    is_active = forms.BooleanField(label='Is Active')
    is_manager = forms.BooleanField(label='Is Manager')


class CustomUserChangeForm(forms.ModelForm):
    """
    一个自定义的用户更改表单，用于Django的admin界面或类似界面中修改用户信息。

    Attributes:
        fields (list): 表单中包含的字段列表。此处指定了包含的字段及其顺序。
    """

    class Meta:
        """
        表单的元数据，指定了使用的模型和表单字段。

        Attributes:
            model (User): 表单关联的模型类，此处为CustomUser模型。
            fields (list): 表单中包含的字段列表，指定了需要在表单中显示和修改的字段。
        """
        model = User  # 指定使用的模型
        fields = ['full_name', 'email', 'password','is_active', 'is_manager']  # 指定表单中包含的字段

    def __init__(self, *args, **kwargs):
        """
        初始化表单实例。

        Args:
            *args: 位置参数，传递给父类的构造器。
            **kwargs: 关键字参数，传递给父类的构造器。
        """
        super().__init__(*args, **kwargs)
        # 为每个字段的输入小部件添加HTML属性，如class和placeholder
        self.fields['full_name'].widget.attrs.update({'class': 'form-control', 'placeholder': _('请输入昵称')})
        self.fields['email'].widget.attrs.update({'class': 'form-control', 'placeholder': _('请输入电子邮件')})
        self.fields['password'].widget.attrs.update({'class': 'form-control', 'placeholder': _('请输入密码')})
        # 更改特定字段的标签
        self.fields['full_name'].label = _('昵称')
        self.fields['email'].label = _('电子邮件')
        self.fields['password'].label = _('密码')
        self.fields['is_active'].label = _('是否活跃')
        self.fields['is_manager'].label = _('是否为管理员')

    def save(self, commit=True):
        """
        保存表单数据到模型实例。

        Args:
            commit (bool, optional): 是否立即提交到数据库。默认为True。

        Returns:
            User: 保存后的用户模型实例。
        """
        user = super().save(commit=False)
        # 此处可以添加任何自定义逻辑，以在保存用户实例前对其进行修改或处理
        if commit:
            user.save()  # 如果指定提交，则保存用户实例到数据库
        return user  # 返回保存后的用户实例


