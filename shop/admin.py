from django.contrib import admin

from .models import subscribeform

from .models import Products

from .models import Contact

from .models import category

from .models import Orders

from .models import Customer





class adminproduct(admin.ModelAdmin):
    list_display=('pro_name','price','category','subcategory','pub_date','img')
    search_fields=('pro_name','price','category','subcategory','pub_date')
    list_filter=('price','category','subcategory','pub_date')


class admincategory(admin.ModelAdmin):
    list_display=['name']

class adminorder(admin.ModelAdmin):
    list_display=('customer','Email','product','quantity','price','address','state','city','date')
    search_fields=('customer','Email','product','qunantity','price','address','state','city','date')
    list_filter=('customer','Email','product','quantity','price','address','state','city','date')

class admincustomer(admin.ModelAdmin):
    list_display=('first_name','last_name','email')
    search_fields=('first_name','last_name','email')
    list_filter=('first_name','last_name','email')
  
   

admin.site.register(Products, adminproduct)

admin.site.register(subscribeform)

admin.site.register(Contact)

admin.site.register(Orders,adminorder)

admin.site.register(Customer,admincustomer)

admin.site.register(category, admincategory)



# Register your models here.
