from django.contrib import admin
from .models import *


# Define the admin options for the Customer table
class CustomerList(admin.ModelAdmin):
    list_display = ('cust_name', 'organization', 'phone')
    list_filter = ('cust_name', 'organization')

    # borrowed concept from Assign 1
    fieldsets = (
        ('Personal Details', {
            'fields': ('cust_name', 'organization', 'role', 'bldgroom')
        }),

        ('Contact Details', {
            'fields': ('address', 'city', 'state', 'zipcode', 'phone', 'email')
        }),
    )
    search_fields = ('cust_name',)
    ordering = ['cust_name']


# Define the admin options for the Service table
class ServiceList(admin.ModelAdmin):
    list_display = ('cust_name', 'service_category', 'setup_time')
    list_filter = ('cust_name', 'setup_time')
    search_fields = ('service_category', 'cust_name',)
    ordering = ['cust_name']


# Define the admin options for the Product table
class ProductList(admin.ModelAdmin):
    list_display = ('cust_name', 'product', 'quantity', 'pickup_time')
    list_filter = ('cust_name', 'pickup_time')
    fieldsets = (
        ('Customer Details', {
            'fields': ('cust_name',)
        }),

        ('Product Details', {
            'fields': ('product', 'quantity', 'charge', 'pickup_time',)
        }),
    )

    search_fields = ('product', 'cust_name')
    ordering = ['cust_name']


# register the Service and Product with the django admin page
admin.site.register(Customer, CustomerList)
admin.site.register(Service, ServiceList)
admin.site.register(Product, ProductList)
