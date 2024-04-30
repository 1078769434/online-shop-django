from django.contrib.auth.models import BaseUserManager


class UserManager(BaseUserManager):
    """
    自定义用户管理器，继承自Django的BaseUserManager。
    """

    def create_user(self, email, full_name, password):
        """
        创建一个普通用户账号。

        参数:
        - email: 用户的电子邮箱地址，唯一标识一个用户。
        - full_name: 用户的全名。
        - password: 用户的密码。

        返回值:
        - 创建成功的用户实例。

        异常:
        - 如果email或full_name为空，则抛出ValueError。
        """
        if not email:
            raise ValueError('Email is required!')
        if not full_name:
            raise ValueError('full name is required!')

        # 创建用户实例并设置属性
        user = self.model(email=self.normalize_email(email), full_name=full_name)
        user.set_password(password)  # 对密码进行加密处理
        user.save(using=self.db)  # 保存用户到数据库
        return user

    def create_superuser(self, email, full_name, password):
        """
        创建一个超级管理员用户账号。

        参数:
        - email: 超级管理员的电子邮箱地址。
        - full_name: 超级管理员的全名。
        - password: 超级管理员的密码。

        返回值:
        - 创建成功的超级管理员用户实例。
        """
        user = self.create_user(email, full_name, password)  # 创建普通用户实例

        # 将用户标记为超级管理员
        user.is_admin = True
        user.save(using=self.db)  # 保存至数据库
        return user

