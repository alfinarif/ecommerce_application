from django import template
from store.models import Category, Product

register = template.Library()

@register.filter
def cat_tabs(pk):
    get_cat = Category.objects.get(id=pk)
    cat_product = Product.objects.filter(category=get_cat).order_by('-id')
    if cat_product.exists():
        return cat_product
    else:
        return cat_product