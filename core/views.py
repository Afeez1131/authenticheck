from django.shortcuts import render, get_object_or_404
from django.views.generic.edit import CreateView, UpdateView, DeleteView, FormView
from django.views.generic import DetailView, TemplateView, ListView
from .models import Business, Product, ProductInstance
from braces.views import LoginRequiredMixin
from .forms import BusinessForm
from datetime import datetime
import logging

logger = logging.getLogger(__name__)

class DashboardView(LoginRequiredMixin, TemplateView):
    template_name = "core/dashboard.html"

    def get_context_data(self, **kwargs):
        context = super(DashboardView, self).get_context_data(**kwargs)
        logger.info("in the dashboard")
        user = self.request.user
        business =  get_object_or_404(Business, user=user)
        products = business.product_set.all()
        instances_created_today = ProductInstance.objects.filter(created__date=datetime.now().date()).count()
        recent_instances = ProductInstance.objects.all()[:10]
        context['product_count'] = products.count()
        context['instances_created_today'] = instances_created_today
        context['recent_instances'] = recent_instances
        context['business'] = business
        return context
    
dashboard = DashboardView.as_view()


class ProductsView(LoginRequiredMixin, CreateView, ListView):
    model = Product
    template_name = "core/product.html"
    paginate_by = 100
    context_object_name = "products"

    def get_queryset(self):
        queryset = super(ProductsView, self).get_queryset()
        return queryset

    def get_context_data(self, **kwargs):
        self.object_list = self.get_queryset()
        context = super().get_context_data(*kwargs)
        return context

    def get_success_url(self):
        messages.success(request, "Product Created successfully")
        pass


class ProductInstanceView(LoginRequiredMixin, CreateView, ListView):
    model = Product
    template_name = "core/product_instance.html"
    paginate_by = 100
    context_object_name = "product_instances"

    def get_queryset(self):
        queryset = super(ProductInstanceView, self).get_queryset()
        return queryset

    def get_context_data(self, **kwargs):
        self.object_list = self.get_queryset()
        context = super().get_context_data(*kwargs)
        return context

    def get_success_url(self):
        messages.success(request, "Product Instance Created successfully")
        pass
    
product_instant = ProductInstanceView.as_view()