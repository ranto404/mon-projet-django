# Generated by Django 5.0.4 on 2024-05-31 14:13

import django.db.models.deletion
import shortuuid.django_fields
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('AppInscription', '0001_initial'),
        ('Apphome', '0004_category_alter_produit_image'),
    ]

    operations = [
        migrations.CreateModel(
            name='CardOrder',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('price', models.DecimalField(decimal_places=2, default='00', max_digits=999999999999)),
                ('paid_status', models.BooleanField(default=False)),
                ('order_date', models.DateTimeField(auto_now_add=True)),
                ('product_status', models.CharField(choices=[('process', 'Processing'), ('shipped', 'Shipped'), ('delivered', 'Delivered')], default='processig', max_length=10)),
            ],
            options={
                'verbose_name_plural': 'Card Order',
            },
        ),
        migrations.CreateModel(
            name='CardOrderItems',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('invoice_no', models.CharField(max_length=200)),
                ('product_status', models.CharField(max_length=200)),
                ('item', models.CharField(max_length=200)),
                ('image', models.CharField(max_length=200)),
                ('quantity', models.IntegerField(default='0')),
                ('price', models.DecimalField(decimal_places=2, default='00', max_digits=999999999999)),
                ('total', models.DecimalField(decimal_places=2, default='000', max_digits=999999999999)),
                ('order', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Apphome.cardorder')),
            ],
            options={
                'verbose_name_plural': 'Card Order Items',
            },
        ),
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('pid', shortuuid.django_fields.ShortUUIDField(alphabet='abcdef12345', length=10, max_length=20, prefix='cat', unique=True)),
                ('titre', models.CharField(max_length=255)),
                ('description', models.TextField()),
                ('image', models.ImageField(upload_to='static/img/prods')),
                ('price', models.DecimalField(decimal_places=2, default='0.00', max_digits=999999999999)),
                ('old_price', models.DecimalField(decimal_places=2, default='0.00', max_digits=999999999999)),
                ('product_status', models.CharField(choices=[('draft', 'Draft'), ('disabled', 'Disabled'), ('rejected', 'Rejected'), ('in_review', 'In Review'), ('published', 'Published')], default='in_review', max_length=255)),
                ('status', models.BooleanField(default=True)),
                ('in_stock', models.BooleanField(default=True)),
                ('featured', models.BooleanField(default=False)),
                ('digital', models.BooleanField(default=False)),
                ('sku', shortuuid.django_fields.ShortUUIDField(alphabet='1234567890', length=4, max_length=200, prefix='sku', unique=True)),
                ('date', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(blank=True, null=True)),
            ],
            options={
                'verbose_name_plural': 'Products',
            },
        ),
        migrations.CreateModel(
            name='ProductImages',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('images', models.ImageField(default='product.jpg', upload_to='product-images')),
                ('date', models.DateTimeField(auto_now_add=True)),
            ],
            options={
                'verbose_name_plural': 'Product Images',
            },
        ),
        migrations.CreateModel(
            name='ProductReview',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('review', models.TextField()),
                ('rating', models.IntegerField(choices=[(1, '⭐☆☆☆☆'), (2, '⭐⭐☆☆☆'), (3, '⭐⭐⭐☆☆'), (4, '⭐⭐⭐⭐☆'), (5, '⭐⭐⭐⭐⭐')], default=None)),
                ('date', models.DateTimeField(auto_now_add=True)),
            ],
            options={
                'verbose_name_plural': 'Product Reviews',
            },
        ),
        migrations.CreateModel(
            name='Vendor',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('vid', shortuuid.django_fields.ShortUUIDField(alphabet='abcdef12345', length=10, max_length=20, prefix='cat', unique=True)),
                ('title', models.CharField(max_length=100)),
                ('image', models.ImageField(upload_to='static/img/category')),
                ('description', models.TextField(blank=True, null=True)),
                ('adresse', models.TextField(default='123 Main Tree', max_length=100)),
                ('contacte', models.TextField(default='+123 (456) 789', max_length=100)),
                ('chat_resp_time', models.TextField(default='100', max_length=100)),
                ('shipping_on_time', models.TextField(default='100', max_length=100)),
                ('authentic_rating', models.TextField(default='100', max_length=100)),
                ('days_return', models.TextField(default='100', max_length=100)),
                ('warranty_period', models.TextField(default='100', max_length=100)),
                ('user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='AppInscription.membres')),
            ],
            options={
                'verbose_name_plural': 'Vendors',
            },
        ),
        migrations.CreateModel(
            name='Wishlist',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateTimeField(auto_now_add=True)),
            ],
            options={
                'verbose_name_plural': 'Wishlists',
            },
        ),
        migrations.DeleteModel(
            name='Produit',
        ),
        migrations.AlterModelOptions(
            name='category',
            options={'verbose_name_plural': 'Categories'},
        ),
        migrations.AddField(
            model_name='category',
            name='image',
            field=models.ImageField(default='category.jpg', upload_to='static/img/category'),
        ),
        migrations.AddField(
            model_name='category',
            name='name',
            field=models.CharField(default=1, max_length=255),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='category',
            name='title',
            field=models.CharField(default='Categorie', max_length=100),
        ),
        migrations.AddField(
            model_name='product',
            name='category',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='Apphome.category'),
        ),
        migrations.AddField(
            model_name='productimages',
            name='product',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='Apphome.product'),
        ),
        migrations.AddField(
            model_name='productreview',
            name='product',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='Apphome.product'),
        ),
        migrations.AddField(
            model_name='wishlist',
            name='product',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='Apphome.product'),
        ),
    ]
