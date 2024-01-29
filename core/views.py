from django.shortcuts import render, get_object_or_404
from django.urls import reverse, reverse_lazy
from django.views.generic.edit import CreateView, UpdateView, DeleteView, FormView
from django.views.generic import DetailView, TemplateView, ListView

from core.utils import redirect_to_referrer, top_nine_product
from .models import Business, Product, ProductInstance
from braces.views import LoginRequiredMixin
from .forms import BusinessForm, ProductForm, ProductInstanceForm
from datetime import datetime, timedelta
from django.contrib import messages
from django.db.models import Count
from django.utils.safestring import mark_safe
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseRedirect
import logging

logger = logging.getLogger(__name__)

class DashboardView(LoginRequiredMixin, TemplateView):
    template_name = "core/dashboard.html"

    def get_context_data(self, **kwargs):
        context = super(DashboardView, self).get_context_data(**kwargs)
        user = self.request.user
        business =  get_object_or_404(Business, user=user)
        products = business.product_set.all()
        instances_created_today = ProductInstance.objects.filter(product__business__user=user, created__date=datetime.now().date()).count()
        recent_instances = ProductInstance.objects.filter(product__business__user=user).order_by('-created')[:10]
        context['top_nine_product'] = top_nine_product(user.id)
        context['product_count'] = products.count()
        context['instances_created_today'] = instances_created_today
        context['recent_instances'] = recent_instances
        context['business'] = business
        return context
    
dashboard = DashboardView.as_view()


class CreateProfileView(LoginRequiredMixin, CreateView):
    template_name = "core/create_profile.html"
    form_class = BusinessForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context
    
    def get_success_url(self):
        messages.success(self.request, 'Business Profile Created.')
        return reverse_lazy('core:profile')
    
    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)

create_profile = CreateProfileView.as_view()


class UpdateProfileView(LoginRequiredMixin, UpdateView):
    form_class = BusinessForm
    model = Business
    template_name = "core/profile.html"
    # success_url = reverse_lazy('core:profile')
    
    def get_success_url(self):
        messages.success(self.request, 'Profile Updated Successfully.')
        return reverse_lazy('core:profile')
    
    def get_object(self, queryset=None):
        return get_object_or_404(Business, user=self.request.user)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        business = get_object_or_404(Business, user=self.request.user)
        context['business'] = business
        # context['form'] = self.form_class(instance=business)
        return context

business_profile = UpdateProfileView.as_view()


class ProductsView(LoginRequiredMixin, CreateView, ListView):
    model = Product
    template_name = "core/product.html"
    form_class = ProductForm
    paginate_by = 100
    context_object_name = "products"

    def get_queryset(self):
        queryset = super(ProductsView, self).get_queryset()
        return queryset.filter(business__user=self.request.user)

    def get_context_data(self, **kwargs):
        self.object_list = self.get_queryset()
        context = super().get_context_data(**kwargs)
        context['edit_form'] = ProductForm(prefix="edit")
        return context

    def get_success_url(self):
        messages.success(self.request, "Product Created successfully")
        return reverse_lazy("core:products")
    
    def form_valid(self, form):
        business = get_object_or_404(Business, user=self.request.user)
        form.instance.business = business
        return super().form_valid(form)

products = ProductsView.as_view()


@login_required
def update_product(request):
    if not request.method == 'POST' or not request.POST.get('pid'):
        messages.error(request, 'Invalid Request')
        return HttpResponseRedirect(redirect_to_referrer(request, reverse('core:products')))
    pid = request.POST.get('pid', '')
    product = get_object_or_404(Product, id=pid)
    name = product.name
    form = ProductForm(request.POST, instance=product, prefix="edit")
    if form.is_valid():
        form.save()
        messages.success(request, f'{name} successfully updated.')
    else:
        messages.error(request, form.errors)
    return HttpResponseRedirect(reverse('core:products'))


@login_required
def delete_product(request):
    if not request.method == 'POST' or not request.POST.get('pid'):
        messages.error(request, 'Invalid Request')
        return HttpResponseRedirect(redirect_to_referrer(request, reverse('core:products')))
    pid = request.POST.get('pid', '')
    product = get_object_or_404(Product, id=pid)
    name = product.name
    product.delete()
    messages.success(request, f'{name} successfully Deleted.')
    return HttpResponseRedirect(reverse('core:products'))
        

class ProductInstanceView(LoginRequiredMixin, CreateView, ListView):
    model = ProductInstance
    template_name = "core/product_instance.html"
    paginate_by = 100
    form_class = ProductInstanceForm
    context_object_name = "product_instances"

    def get_queryset(self):
        queryset = super(ProductInstanceView, self).get_queryset()
        pk = self.kwargs.get('pk', '')
        product = get_object_or_404(Product, pk=pk)
        return queryset.filter(product=product)

    def get_context_data(self, **kwargs):
        self.object_list = self.get_queryset()
        context = super().get_context_data(**kwargs)
        pk = self.kwargs.get('pk', '')
        product = get_object_or_404(Product, pk=pk)
        context["edit_form"] = ProductInstanceForm(initial={'product': product}, prefix="edit")
        context['product'] = product
        return context

    def get_success_url(self):
        pk = self.kwargs.get('pk', '')
        product = get_object_or_404(Product, pk=pk)
        messages.success(self.request, "Product Instance Created successfully")
        return reverse_lazy("core:product_instances", args=[product.pk])
    
    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        pk = self.kwargs.get('pk', '')
        product = get_object_or_404(Product, pk=pk)
        kwargs['initial'].update({'product': product})
        return kwargs
    
    def form_valid(self, form):
        pk = self.kwargs.get('pk', '')
        product = get_object_or_404(Product, pk=pk)
        form.instance.product = product
        return super().form_valid(form)
    
    def form_invalid(self, form):
        messages.error(self.request, form.errors)
        return super().form_invalid(form)
    
product_instances = ProductInstanceView.as_view()


@login_required
def update_product_instance(request):
    if not request.method == 'POST' or not request.POST.get('instance_id', ''):
        messages.error(request, "invalid request")
        return HttpResponseRedirect(redirect_to_referrer(request, reverse('core:products')))
    instance_id = request.POST.get('instance_id', '')
    instance = get_object_or_404(ProductInstance, pk=instance_id,)
    form = ProductInstanceForm(request.POST, instance=instance, prefix='edit')
    if form.is_valid():
        form.save()
        messages.success(request, 'Instance Updated successfully.')
    else:
        messages.error(request, form.errors)
    return HttpResponseRedirect(reverse('core:product_instances', args=[instance.product.pk]))
    
    
@login_required
def delete_product_instance(request):
    url = redirect_to_referrer(request, reverse('core:products'))
    if request.method != 'POST' or not request.POST.get('instance_id', ''):
        messages.error(request, 'Invalid request')
        return HttpResponseRedirect(url)
    instance_id = request.POST.get('instance_id', '')
    instance = get_object_or_404(ProductInstance, id=instance_id)
    instance.delete()
    messages.success(request, 'Instance successfully deleted')
    return HttpResponseRedirect(url)


def http_500(request):
    obj = get_object_or_404(Product, name__icontains='Pro')
    return HttpResponse(f"hello world {obj}")


    """
    QR CODE GENERATION 
    """
