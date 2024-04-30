# 导入必要的模块
from django.urls import path, reverse_lazy
from django.contrib.auth import views as auth_views

# 从accounts模块导入视图
from accounts import views
from accounts.views import manage_shipping_address

# 定义app的名称
app_name = 'accounts'

# 定义URL模式
urlpatterns = [
    # 用户注册页面
    path('register/', views.user_register, name='user_register'),
    # 用户登录页面
    path('login/', views.user_login, name='user_login'),
    # 管理员登录页面
    path('login/manager/', views.manager_login, name='manager_login'),
    # 用户登出
    path('logout/', views.user_logout, name='user_logout'),
    # 编辑用户资料
    path('profile/edit', views.edit_profile, name='edit_profile'),
    # 管理配送地址
    path('profile/manage_shipping_address', views.manage_shipping_address, name='manage_shipping_address'),

    # # 添加地址URL
    # path('shipping-address/add/', views.add_shipping_address, name='add_shipping_address'),
    #
    # # 编辑地址URL（使用地址ID作为参数）
    # path('shipping-address/edit/<int:address_id>/', views.edit_shipping_address, name='edit_shipping_address'),
    #
    # # 删除地址URL（使用地址ID作为参数）
    # path('shipping-address/delete/<int:address_id>/', views.delete_shipping_address, name='delete_shipping_address'),

    # 忘记密码：重置密码请求页面
    path(
        'password-reset/',
        auth_views.PasswordResetView.as_view(
            template_name='password_reset.html',
            success_url=reverse_lazy('accounts:password_reset_done'),
            email_template_name='email_template.html'
        ),
        name='password_reset'
    ),
    # 忘记密码：重置密码请求成功页面
    path(
        'password-reset/done',
        auth_views.PasswordResetDoneView.as_view(
            template_name='password_reset_done.html',
        ),
        name='password_reset_done'
    ),
    # 忘记密码：确认重置密码页面
    path(
        'password-reset-confirm/<uidb64>/<token>/',
        auth_views.PasswordResetConfirmView.as_view(
            template_name='password_reset_confirm.html',
            success_url=reverse_lazy('accounts:password_reset_complete'),
        ),
        name='password_reset_confirm'
    ),
    # 忘记密码：重置密码完成页面
    path(
        'password-reset-complete/',
        auth_views.PasswordResetCompleteView.as_view(
            template_name='password_reset_complete.html',
        ),
        name='password_reset_complete'
    ),
]
