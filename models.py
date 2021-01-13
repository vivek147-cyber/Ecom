from django.db import models
import datetime
from django.core.validators import MinLengthValidator

from django.contrib.auth.models import User




class subscribeform(models.Model):
    email=models.CharField(max_length=50)

    def __str__(self):
       return self.email 

class category(models.Model):
    name=models.CharField(max_length=50)

    def __str__(self):
       return self.name

class Products(models.Model):
    pro_id=models.AutoField
    pro_name=models.CharField(max_length=20)
    pro_desc=models.TextField()
    pro_Info=models.TextField(default="")
    pro_key=models.TextField(default="")
    color=models.CharField(max_length=10,default="",blank=True)
    size=models.CharField(max_length=10,default="",blank=True)
    availability=models.CharField(max_length=10,default="")
    category=models.ForeignKey(category,on_delete=models.CASCADE,default=1,null=False)
    subcategory=models.CharField(max_length=40,default="")
    price=models.IntegerField(default=0)
    pub_date=models.DateField()
    img=models.ImageField(upload_to="shop/images",default="")

    
    @staticmethod
    def get_products_by_id(ids):
        return Products.objects.filter(id__in =ids)    
     
    
         

    @staticmethod
    def get_all_product_by_category_id(category_id):
        if category_id:
            return Products.objects.filter(category=category_id)
        else:
            return Products.objects.all();    

    def __str__(self):
       return (self.pro_name)
      

class Customer(models.Model):
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    email = models.EmailField()
    password = models.CharField(max_length=500)

    def __str__(self):
       return (self.first_name)

    def register(self):
        self.save()

    @staticmethod
    def get_customer_by_email(email):
        try:
            return Customer.objects.get(email=email)
        except:
            return False

    def isExists(self):
        if Customer.objects.filter(email = self.email):
            return True

        return  False


class Orders(models.Model):
    product=models.ForeignKey(Products,on_delete=models.CASCADE)
    customer=models.ForeignKey(Customer,on_delete=models.CASCADE)
    Name=models.CharField(max_length=30,default="")
    Email=models.CharField(max_length=50,default="")
    quantity=models.IntegerField(default=1)
    price=models.IntegerField(default=1,null=False)
    address=models.CharField(max_length=100,default="")
    phone=models.IntegerField(default=1)
    country=models.CharField(max_length=15,default="")
    state=models.CharField(max_length=15,default="")
    city=models.CharField(max_length=15,default="")
    Pincode=models.IntegerField()
    date=models.DateField(default=datetime.datetime.today)
    status=models.BooleanField(default=False)

    def placeOrder(self):
        self.save()

    @staticmethod
    def get_orders_by_customer(customer_id):
        return Orders.objects.filter(customer=customer_id).order_by('-id')
   
    
    

class Contact(models.Model):
    no=models.AutoField
    fname=models.CharField(max_length=10)
    Phone=models.IntegerField()
    email=models.CharField(max_length=20)
    message=models.TextField(default="")
    timestamp=models.DateTimeField(auto_now_add=True,blank=True)

    def __str__(self):
       return self.fname
# Create your models here.
