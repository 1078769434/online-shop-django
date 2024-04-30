import os

from django.core.wsgi import get_wsgi_application
from accounts.views import create_manager

# 设置Django环境变量
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'online_shop.settings')

# 创建具有 'manager' 角色的用户
create_manager()

# 获取WSGI应用实例
application = get_wsgi_application()
