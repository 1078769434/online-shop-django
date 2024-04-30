# 从django.contrib导入admin模块
from django.contrib import admin

# 从当前模块导入User模型
from .models import User

# 将User模型注册到Django的后台管理系统中
admin.site.register(User)
