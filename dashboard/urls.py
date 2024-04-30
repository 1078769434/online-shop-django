from django.urls import path

from dashboard import views

app_name = 'dashboard'

urlpatterns = [
    path('products', views.products, name='products'),
    path('products/delete/<int:id>', views.delete_product, name='delete_product'),
    path('products/edit/<int:id>', views.edit_product, name='edit_product'),
    path('orders', views.orders, name='orders'),
    path('orders/detail/<int:id>', views.order_detail, name='order_detail'),
    path('add-product/', views.add_product, name='add_product'),
    path('add-category/', views.add_category, name='add_category'),

    path('users/', views.users, name='users'),
    path('add-user/', views.add_user, name='add_user'),
    path('edit-user/<int:user_id>/', views.edit_user, name='edit_user'),
    path('delete-user/<int:user_id>/', views.delete_user, name='delete_user'),
]
