from django.conf.urls.static import static
from django import views
from django.contrib import admin
from django.urls import path
from django.conf import settings
from myapp.views import add_to_cart, category_list, checkout, order_confirmation, product_detail, product_list, register,  remove_from_cart, user_login, user_logout, view_cart

urlpatterns = [
    path('admin/', admin.site.urls),
    path('cat', category_list, name='category_list'),
    path('', product_list, name='product_list'),
    path('products/<int:category_id>/', product_list, name='product_list'),
    path('product/<int:pk>/', product_detail, name='product_detail'),
    path('cart/', view_cart, name='cart'),
    path('cart/add/<int:pk>/', add_to_cart, name='add_to_cart'),
    path('cart/remove/<int:pk>/', remove_from_cart, name='remove_cart_item'),
    path('checkout/', checkout, name='checkout'),
    path('order_confirmation/', order_confirmation, name='order_confirmation'),
     path('register/', register, name='register'),
    path('login/', user_login, name='login'),

    path('logout/', user_logout, name='logout'),
]


# Include static and media file-serving for development
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
