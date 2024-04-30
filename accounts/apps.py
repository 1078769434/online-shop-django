# 该模块定义了一个自定义的应用配置类，用于Django框架中的accounts应用。

from django.apps import AppConfig


class AccountsConfig(AppConfig):
    """
    AccountsConfig类继承自Django的AppConfig类，用于自定义应用配置。

    属性:
    - default_auto_field: 指定模型中自动字段的默认类型为BigAutoField，即使用64位的整数作为主键。
    - name: 应用的名称，这里指定为'accounts'。
    """
    default_auto_field = 'django.db.models.BigAutoField'  # 指定默认的自动增长字段类型为BigAutoField
    name = 'accounts'  # 指定配置对应的app名称

