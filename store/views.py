from django.db import models
from django.shortcuts import render
# django generic view
from django.views.generic import ListView, DetailView, TemplateView
# import models
from store.models import Category, Product, Banner


# store index class view
class IndexProductListView(ListView):
    model = Product
    context_object_name = 'products'
    template_name = 'store/index2.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['banners'] = Banner.objects.all().order_by('-id')
        return context

# product details class view
class ProductDetailsView(DetailView):
    model = Product
    context_object_name = 'product'
    template_name = 'store/product.html'
