from django.shortcuts import render
from django.views.generic.edit import CreateView, UpdateView, DeleteView, FormView
from django.views.generic import DetailView
from .models import Business, Product, ProductInstance
from braces.views import LoginRequiredMixin
from .forms import BusinessForm


class CreateBusiness(LoginRequiredMixin, CreateView):
    model = Business
    form_class = BusinessForm
    template_name = "core/create_business.html"