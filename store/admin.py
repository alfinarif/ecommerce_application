from django.contrib import admin
from store.models import Category, Brand, Product, ProductImageGallery, Variation, Banner, Review

# variation
class VariationAdmin(admin.StackedInline):
    model = Variation

# image gallery
class ProductImageGalleryAdmin(admin.StackedInline):
    model = ProductImageGallery


# product admin class
class ProductAdmin(admin.ModelAdmin):
    inlines = [VariationAdmin, ProductImageGalleryAdmin]
    prepopulated_fields = {'slug': ('name',)}


# Register your models here.
# banners
admin.site.register(Banner)
admin.site.register(Product, ProductAdmin)
admin.site.register(Category)
admin.site.register(Brand)
admin.site.register(Review)
