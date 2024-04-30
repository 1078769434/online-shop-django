# 导入必要的模块
import os

# 从Django的core模块导入get_asgi_application函数
from django.core.asgi import get_asgi_application

# 设置环境变量，指定Django的设置模块，默认为'online_shop.settings'
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'online_shop.settings')

# 获取并定义ASGI应用程序实例
application = get_asgi_application()
