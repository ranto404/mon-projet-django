# Generated by Django 5.0.4 on 2024-06-13 13:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Apphome', '0007_cardorder_user'),
    ]

    operations = [
        migrations.CreateModel(
            name='Cart',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('products', models.ManyToManyField(to='Apphome.product')),
            ],
        ),
    ]
