from django.db import models
from django.urls import reverse
from django.template.defaultfilters import slugify


# category model class
class Category(models.Model):
    parent = models.ForeignKey('self', related_name='children', on_delete=models.CASCADE, blank=True, null=True)
    name = models.CharField(max_length=30)
    image = models.ImageField(upload_to='category', null=True, blank=True)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['-created', ]
        verbose_name_plural = 'Categories'

# brand models class
class Brand(models.Model):
    name = models.CharField(max_length=50)
    image = models.ImageField(upload_to='brand', null=True, blank=True)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['-created', ]
        verbose_name_plural = 'Brand'


# product model class
class Product(models.Model):
    PRODUCT_STATUS = (
        ('new', 'new'),
        ('hot', 'hot'),
        ('bestseller', 'bestseller'),
    )
    name = models.CharField(max_length=255)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='category')
    brand = models.ForeignKey(Brand, on_delete=models.CASCADE, related_name='brand')
    preview_des = models.TextField(max_length=200, verbose_name='Preview Description')
    description = models.TextField(max_length=1000, verbose_name='Description')
    image = models.ImageField(upload_to='products', null=False, blank=False)
    price = models.FloatField()
    old_price = models.FloatField(default=0.00)
    is_stock = models.BooleanField(default=True)
    status = models.CharField(max_length=50, choices=PRODUCT_STATUS, default='new', blank=True, null=True)
    status_valid = models.DateTimeField()
    slug = models.SlugField()
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

    def get_product_url(self):
        return reverse('store:product_detail', kwargs={'slug': self.slug})
    
    def get_discount_percentage(self):
        discount_percentage = (self.old_price - self.price) / self.old_price * 100
        return int(discount_percentage)
        

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        return super().save(*args, **kwargs)

    class Meta:
        ordering = ['-created', ]
        verbose_name_plural = 'Products'


# product image gallery models class
class ProductImageGallery(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    image = models.FileField(upload_to='product_gallery', null=True, blank=True)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self) -> str:
        return str(self.product.name)

# banner model class
class Banner(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='product_banner')
    image = models.ImageField(upload_to='banner', blank=True, null=True)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self) -> str:
        return self.product.name

# product variation manager models class
class VariationManager(models.Manager):
    def sizes(self):
        return super(VariationManager, self).filter(variation_type='size')
    def colors(self):
        return super(VariationManager, self).filter(variation_type='color')

# product variation models class
class Variation(models.Model):
    VARIATIONS_TYPE = (
        ('size', 'size'),
        ('color', 'color'),
    )
    variation_type = models.CharField(max_length=50, choices=VARIATIONS_TYPE)
    name = models.CharField(max_length=50)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    price = models.IntegerField()
    image = models.ImageField(upload_to='variations', null=True, blank=True)
    created = models.DateTimeField(auto_now_add=True)
    # objects manager
    objects = VariationManager()
    
    def __str__(self) -> str:
        return self.name

    class Meta:
        ordering = ['-created', ]
        verbose_name_plural = 'Product Variations'