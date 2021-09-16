from django.db import models
from django.shortcuts import render
# django generic view
from django.views.generic import ListView, DetailView, TemplateView
# import models
from store.models import Category, Product, Banner, ProductImageGallery, Brand, Review

from datetime import datetime
from django.utils import timezone

# store index class view
class IndexProductListView(TemplateView):
    def get(self, request, *args, **kwargs):
        products = Product.objects.all().order_by('-id')
        banners = Banner.objects.all().order_by('-id')
        categories = Category.objects.all().order_by('-id')
        brands = Brand.objects.all().order_by('-id')
        #updated product new,hot,bestseller status    
        for prod in products:
            if prod.status_valid > prod.created:
                prod.status = None
                prod.save()

        context = {
            'products': products,
            'banners': banners,
            'categories': categories,
            'brands': brands
        }
        return render(request, 'store/index2.html', context)


# product details class view
class ProductDetailsView(DetailView):
    model = Product
    context_object_name = 'product'
    template_name = 'store/detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['product_images'] = ProductImageGallery.objects.filter(product=self.object.id)
        context['category_based'] = Product.objects.filter(category=self.object.category)
        context['reviews'] = Review.objects.filter(product=self.object.id)
        return context











