# Generated by Django 3.0.8 on 2020-12-29 19:07

import datetime
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='category',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name='Contact',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('fname', models.CharField(max_length=10)),
                ('Phone', models.IntegerField()),
                ('email', models.CharField(max_length=20)),
                ('message', models.TextField(default='')),
                ('timestamp', models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name='Customer',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('first_name', models.CharField(max_length=50)),
                ('last_name', models.CharField(max_length=50)),
                ('email', models.EmailField(max_length=254)),
                ('password', models.CharField(max_length=500)),
            ],
        ),
        migrations.CreateModel(
            name='slider',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=20)),
                ('desc', models.CharField(default='', max_length=250)),
                ('category', models.CharField(default='', max_length=40)),
                ('subcategory', models.CharField(default='', max_length=40)),
                ('image', models.ImageField(default='', upload_to='shop/images')),
            ],
        ),
        migrations.CreateModel(
            name='Products',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('pro_name', models.CharField(max_length=20)),
                ('pro_desc', models.TextField()),
                ('pro_Info', models.TextField(default='')),
                ('color', models.CharField(blank=True, default='', max_length=10)),
                ('size', models.CharField(blank=True, default='', max_length=10)),
                ('availability', models.CharField(default='', max_length=10)),
                ('subcategory', models.CharField(default='', max_length=40)),
                ('price', models.IntegerField(default=0)),
                ('pub_date', models.DateField()),
                ('img', models.ImageField(default='', upload_to='shop/images')),
                ('category', models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='shop.category')),
            ],
        ),
        migrations.CreateModel(
            name='Orders',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Name', models.CharField(default='', max_length=30)),
                ('Email', models.CharField(default='', max_length=50)),
                ('quantity', models.IntegerField(default=1)),
                ('price', models.IntegerField(default=1)),
                ('address', models.CharField(default='', max_length=100)),
                ('phone', models.IntegerField(default=1)),
                ('country', models.CharField(default='', max_length=15)),
                ('state', models.CharField(default='', max_length=15)),
                ('city', models.CharField(default='', max_length=15)),
                ('Pincode', models.IntegerField()),
                ('date', models.DateField(default=datetime.datetime.today)),
                ('status', models.BooleanField(default=False)),
                ('customer', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='shop.Customer')),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='shop.Products')),
            ],
        ),
    ]
