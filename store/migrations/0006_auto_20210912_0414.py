# Generated by Django 3.1.6 on 2021-09-12 01:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0005_product_status_valid'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='status',
            field=models.CharField(blank=True, choices=[('new', 'new'), ('hot', 'hot'), ('bestseller', 'bestseller')], default='new', max_length=50, null=True),
        ),
    ]
