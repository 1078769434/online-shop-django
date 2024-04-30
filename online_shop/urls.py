from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static


# 定义Django项目的URL模式
urlpatterns = [
    # 管理员页面的URL模式
    path('admin/', admin.site.urls),
    # 商店页面的URL模式，使用命名空间'shop'
    path('', include('shop.urls', namespace='shop')),
    # 用户账户相关的URL模式，使用命名空间'accounts'
    path('accounts/', include('accounts.urls', namespace='accounts')),
    # 购物车相关的URL模式，使用命名空间'cart'
    path('cart/', include('cart.urls', namespace='cart')),
    # 订单相关的URL模式，使用命名空间'orders'
    path('orders/', include('orders.urls', namespace='orders')),
    # 用户仪表盘相关的URL模式，使用命名空间'dashboard'
    path('dashboard/', include('dashboard.urls', namespace='dashboard')),
]

# 在DEBUG模式下，添加静态文件的URL模式
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
