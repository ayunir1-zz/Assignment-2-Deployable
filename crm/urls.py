from django.conf.urls import url
from . import views
from django.urls import path, re_path

app_name = 'crm'
urlpatterns = [
    path('', views.home, name='home'),
    re_path(r'^home/$', views.home, name='home'),

    # customers
    path('customers/', views.customer_list, name='customer_list'),
    path('customer/<int:pk>/edit/', views.customer_edit, name='customer_edit'),
    path('customer/<int:pk>/delete/', views.CustomerDelete.as_view(), name='customer_delete'),
    path('customer/<int:pk>/summary/', views.summary, name='summary'),  # customer Summary

    # services
    path('services/', views.service_list, name='service_list'),
    path('service/create/', views.service_new, name='service_new'),
    path('service/<int:pk>/edit', views.service_edit, name='service_edit'),
    path('service/<int:pk>/delete/', views.ServiceDelete.as_view(), name='service_delete'),

    # products
    path('products/', views.product_list, name='product_list'),
    path('product/create/', views.product_new, name='product_new'),
    path('product/<int:pk>/edit', views.product_edit, name='product_edit'),
    path('product/<int:pk>/delete/', views.ProductDelete.as_view(), name='product_delete'),

]
