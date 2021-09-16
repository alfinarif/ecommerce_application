from django.db import models
from django.http.response import HttpResponseRedirect
from django.shortcuts import redirect, render
from django.http import HttpResponseRedirect
# django generic view
from django.views.generic import ListView, DetailView, TemplateView
# import models
from store.models import Category, Product, Banner, ProductImageGallery, Brand, Review
from store.forms import ProductReviewForm

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
    def get(self, request, slug, *args, **kwargs):
        product = Product.objects.get(slug=slug)
        product_images = ProductImageGallery.objects.filter(product=product)
        category_based = Product.objects.filter(category=product.category)
        reviews = Review.objects.filter(product=product)
        form = ProductReviewForm()

        context = {
            'product': product,
            'product_images': product_images,
            'category_based': category_based,
            'reviews': reviews,
            'review_count': reviews.count(),
            'form': form
        }

        return render(request, 'store/detail.html', context)

    def post(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            if request.method == 'post' or request.method == 'POST':
                get_product = request.POST.get('product')
                product = Product.objects.get(id=get_product)
                form = ProductReviewForm(request.POST)
                if form.is_valid():
                    review_form = form.save(commit=False)
                    review_form.user = request.user
                    review_form.product = product
                    review_form.save()
                    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
        else:
            return HttpResponseRedirect(request.META.get('HTTP_REFERER'))










