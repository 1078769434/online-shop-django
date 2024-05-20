# 简单的在线商店:用Django管理产品和订单
![ 2024-04-25 153603.png](https://s2.loli.net/2024/04/25/dhVGI9kF8UyisEl.png)


这个项目目是用Django编写的一个简单但可用的在线商店。该应用程序提供了一个自定义仪表板来管理产品和订单。用户可以喜欢某个产品，将其添加到购物车中，然后进行结账。支持订单处理，但是使用假支付系统处理付款。

[Preview](#app-preview)

## 特征：

在这个应用程序中有两种类型的用户:普通用户和管理员。

### 可供用户使用:

- **购物车**: 用户可以管理购物车中的物品。
- **编辑个人信息**: 用户可以更新自己的个人信息。
- **订单**: 用户可以查看自己的订单历史。
- **收藏夹**: 用户可以喜欢和保存自己喜欢的产品。
- **重置密码**: 用户可以通过注册邮箱重置密码。

### 可供管理员使用:

管理员可以通过自定义仪表板访问普通用户可用的所有功能，以及其他功能：[http://127.0.0.1:8000/accounts/login/manager](http://127.0.0.1:8000/accounts/login/manager).

- **添加产品**: 经理可以向商店添加新产品。
- **修改和删除产品**: 管理人员可以修改或删除现有产品。
- **添加新分类**: 管理者有能力为产品创造新的类别。
- **获取订单**: 管理员可以查看和管理所有订单和订单项目。

## 技术的使用

- Python 3
- Django
- Bootstrap
- SQLite3 database

## 如何运行应用程序

1. 将项目克隆或下载到本地机器上。
2. 将目录改为"online-shop-django"文件夹。
3. 确保您的机器上安装了Python 3、pip和virtualenv。
4. 使用如下命令创建虚拟环境:
   - For Mac and Linux: `python3 -m venv venv`
   - For Windows: `python -m venv venv`
5. 激活虚拟环境:
   - For Mac and Linux: `source venv/bin/activate`
   - For Windows: `venv\scripts\activate`
6. 通过运行安装应用程序需求: `pip install -r requirements.txt`
7. 通过执行迁移数据库: `python manage.py migrate`
8. 启动服务器: `python manage.py runserver`
9. 您现在应该可以通过访问: [http://127.0.0.1:8000/](http://127.0.0.1:8000/)

## 管理面板访问

要访问管理人员的自定义仪表板，请使用以下凭据:

- Email: manager@example.com
- Password: managerpass1234







