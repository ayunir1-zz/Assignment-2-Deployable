from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse_lazy
from django.views.generic import DeleteView
from django.db.models import Sum
from _decimal import Decimal


from .models import *
from .forms import *
from django.contrib.auth.decorators import login_required


now = timezone.now()


def home(request):
    return render(request, 'crm/home.html', {'crm': home})


@login_required
def customer_list(request):
    customer = Customer.objects.filter()
    return render(request, 'crm/customer_list.html', {'customers': customer})


@login_required
def customer_edit(request, pk):
    customer = get_object_or_404(Customer, pk=pk)
    if request.method == "POST":
        # update
        form = CustomerForm(request.POST, instance=customer)
        if form.is_valid():
            customer = form.save(commit=False)
            customer.updated_date = timezone.now()
            customer.save()
            customer = Customer.objects.filter()
            return render(request, 'crm/customer_list.html',
                          {'customers': customer})
    else:
        # edit
        form = CustomerForm(instance=customer)
    return render(request, 'crm/customer_edit.html', {'form': form})


# class based view for delete function, eliminated the pop confirmation
class CustomerDelete(LoginRequiredMixin, DeleteView):
    model = Customer
    template_name = 'crm/customer_delete.html'
    success_url = reverse_lazy('customer_list')


# views for Services
@login_required
def service_list(request):
    services = Service.objects.filter(created_date__lte=timezone.now())
    return render(request, 'crm/service_list.html', {'services': services})


@login_required
def service_new(request):
    if request.method == "POST":
        form = ServiceForm(request.POST)
        if form.is_valid():
            service = form.save(commit=False)
            service.created_date = timezone.now()
            service.save()
            services = Service.objects.filter(created_date__lte=timezone.now())
            return render(request, 'crm/service_list.html',
                          {'services': services})
    else:
        form = ServiceForm()

    return render(request, 'crm/service_new.html', {'form': form})


@login_required
def service_edit(request, pk):
    service = get_object_or_404(Service, pk=pk)
    if request.method == "POST":
        form = ServiceForm(request.POST, instance=service)
        if form.is_valid():
            service = form.save()
            service.updated_date = timezone.now()
            service.save()
            services = Service.objects.filter(created_date__lte=timezone.now())
            return render(request, 'crm/service_list.html', {'services': services})
    else:
        form = ServiceForm(instance=service)
    return render(request, 'crm/service_edit.html', {'form': form})


class ServiceDelete(LoginRequiredMixin, DeleteView):
    model = Service
    template_name = 'crm/service_delete.html'
    success_url = reverse_lazy('service_list')


# views for products
@login_required
def product_list(request):
    product = Product.objects.filter()
    return render(request, 'crm/product_list.html', {'products': product})


@login_required
def product_new(request):
    if request.method == "POST":
        form = ProductForm(request.POST)
        if form.is_valid():
            product = form.save(commit=False)
            product.created_date = timezone.now()
            product.save()
            products = Product.objects.filter(created_date__lte=timezone.now())
            return render(request, 'crm/product_list.html',
                          {'products': products})
    else:
        form = ProductForm()

    return render(request, 'crm/product_new.html', {'form': form})


def product_edit(request, pk):
    product = get_object_or_404(Product, pk=pk)
    if request.method == "POST":
        form = ProductForm(request.POST, instance=product)
        if form.is_valid():
            product = form.save()
            product.updated_date = timezone.now()
            product.save()
            products = Product.objects.filter(created_date__lte=timezone.now())
            return render(request, 'crm/product_list.html', {'products': products})
    else:
        form = ProductForm(instance=product)
    return render(request, 'crm/product_edit.html', {'form': form})


class ProductDelete(LoginRequiredMixin, DeleteView):
    model = Product
    template_name = 'crm/product_delete.html'
    success_url = reverse_lazy('product_list')


# summary
@login_required
def summary(request, pk):
    customer = get_object_or_404(Customer, pk=pk)
    services = Service.objects.filter(cust_name=pk)
    products = Product.objects.filter(cust_name=pk)
    sum_service_charge = \
        Service.objects.filter(cust_name=pk).aggregate(Sum('service_charge'))
    sum_product_charge = \
        Product.objects.filter(cust_name=pk).aggregate(Sum('charge'))

    # if no product or service records exist for the customer,
    # change the ‘None’ returned by the query to 0.00
    sumTotal = sum_product_charge.get("charge__sum")
    if sumTotal== None:
        sum_product_charge = {'charge__sum': Decimal('0')}

    sumTotal = sum_service_charge.get("service_charge__sum")
    if sumTotal== None:
        sum_service_charge = {'service_charge__sum': Decimal('0')}

    return render(request, 'crm/summary.html',
                  {'customer': customer,
                   'products': products,
                   'services': services,
                   'sum_service_charge': sum_service_charge,
                   'sum_product_charge': sum_product_charge,

                   })
