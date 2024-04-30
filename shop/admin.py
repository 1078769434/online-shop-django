from django.contrib import admin

# 导入Category和Product模型
from .models import Category, Product

# 将Category模型注册到Django admin站点
admin.site.register(Category)
# 将Product模型注册到Django admin站点
admin.site.register(Product)
