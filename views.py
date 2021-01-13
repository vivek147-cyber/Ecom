from django.shortcuts import render, redirect
from django.http import HttpResponse
from math import ceil
from django.contrib.auth.models import User, auth
from django.contrib.auth import logout, login
from django.contrib import messages
from .models import Products
from .models import subscribeform
from .models import Contact
from .models import category
from .models import Orders
from .models import Customer
from django.views import View
from django.core.validators import validate_email
from django.core.exceptions import ValidationError
import random
from django.contrib.auth.hashers import  check_password
from django.contrib.auth.hashers import make_password
from django.core.mail import send_mail
from django_email_verification import sendConfirm
from django.contrib.sites.shortcuts import get_current_site
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from django.template.loader import render_to_string
from .utils import account_activation_token
from django.urls import reverse
from django.utils.encoding import force_bytes, force_text, DjangoUnicodeDecodeError
from shop.middlewares.auth import auth_middleware


def index(request):

        

    product=request.POST.get('product')
    remove=request.POST.get('remove')
    cart=request.session.get('cart')
    if cart:
        quantity=cart.get(product)
        if quantity==1:
            if remove:
                if quantity==1:
                    cart.pop(product)
                else:
                   cart[product]=quantity-1  
            else:    
                 cart[product]=quantity+1

        else:
         cart[product]=1
    else:
        cart={}
        cart[product]=1
    
    
    request.session['cart']=cart
    print(request.session['cart'])

    cart=request.session.get('cart')
    if not cart:
        request.session.cart={}

    


    allprods=[]
    catprods=Products.objects.values('subcategory','id')
    cats={item['subcategory'] for item in catprods}
    for cat in cats:
      prods=Products.objects.filter(subcategory=cat)
      n=len(prods)
      nslides=n//4 + ceil((n/4)-(n//4))
      allprods.append([prods,range(1,nslides),nslides])

    params={'allprods':allprods}



   # n=len(product)
   # noslides=n//4 + ceil((n/4)-(n//4))
   # param={'no_of_slides':noslides, 'range':range(1,noslides), 'Products':Product}
    return render(request, 'shop/index.html', params)

def about(request):
    if request.method=='GET':
        return render(request,'shop/about.html')
    else:

      if request.method=='POST':
        email=request.POST['email']
        subscribe=subscribeform(email=email)

        if len(subscribe.email) < 5:
            error_message = 'email must be 5 char long'

        error_message = None

      if not error_message:
       subscribe.save()
       send_mail(
                'Ecom',
                'Thankyou for Subscribing',
                'from@example.com',
                [email],
                fail_silently=False,)  
       return redirect('about')
      else:
       return render(request,'shop/about.html',{'error': error_message})
    

def contact(request):
    if request.method=='GET':
        return render(request, 'shop/contact.html')
    else:
     if request.method=='POST':
       fname=request.POST.get('text')
       Phone=request.POST.get('phone')
       email=request.POST.get('email')
       message=request.POST.get('content')

       

       contact = Contact(fname=fname,
                            Phone=Phone,
                            email=email,
                           message=message)
       value = {
            'fname': fname,
            'Phone': Phone,
            'email': email,
            'message':message
        }

        
       error_message = None

       if (not contact.fname):
            error_message = "First Name Required !!"
       elif len(contact.fname) < 4:
            error_message = 'First Name must be 4 char long or more'
       elif len(contact.email) < 5:
            error_message = 'email must be 5 char long'
       elif len(contact.Phone) > 10:
            error_message = 'phone number is not valid'
       elif len(contact.Phone.isnumeric()):
            error_message = 'phone number is not valid'

    if not error_message:
       contact.save()
       send_mail(
                'Ecom',
                'Thankyou for sharing your feedback',
                'from@example.com',
                [email],
                fail_silently=False,)  
       return redirect('ShopHome')
    else:
       data = {
                'error': error_message,
                'values': value
            }
       return render(request,'shop/contact.html',data)

def categories(request):

    product=request.POST.get('product')
    remove=request.POST.get('remove')
    cart=request.session.get('cart')
    if cart:
        quantity=cart.get(product)
        if quantity:
            if remove:
                if quantity==1:
                    cart.pop(product)
                else:
                   cart[product]=quantity-1  
            else:    
                 cart[product]=quantity+1

        else:
         cart[product]=1
    else:
        cart={}
        cart[product]=1
    
    
    request.session['cart']=cart
    print(request.session['cart'])

    cart=request.session.get('cart')
    if not cart:
        request.session.cart={}
    

    
    prod=None
    catprods=category.objects.all()
    categoryID=request.GET.get('category')

    if categoryID:
        prod=Products.get_all_product_by_category_id(categoryID)
    else:
        prod=Products.objects.all()

    params={}
    params['prod']=prod
    params['catprods']=catprods


    return render(request,'shop/category.html',params)


def signup(request):
    if request.method=='GET':
        return render(request, 'shop/signup.html')
    else:
        if request.method=='POST':
         first_name=request.POST.get('fname')
         last_name=request.POST.get('lname')
         email=request.POST.get('email')
         password=request.POST.get('pass')


        value = {
            'first_name': first_name,
            'last_name': last_name,
            'email': email
        }
        customer = Customer(first_name=first_name,
                            last_name=last_name,
                            email=email,
                            password=password)

        
        error_message = None

        if (not customer.first_name):
            error_message = "First Name Required !!"
        elif len(customer.first_name) < 4:
            error_message = 'First Name must be 4 char long or more'
        elif not customer.last_name:
            error_message = 'Last Name Required'
        elif len(customer.last_name) < 4:
            error_message = 'Last Name must be 4 char long or more'
        elif len(customer.password) < 6:
            error_message = 'Password must be 6 char long'
        elif len(customer.email) < 5:
            error_message = 'Email must be 5 char long'
        elif customer.isExists():
            error_message = 'Email Address Already Registered..'

    

    if not error_message:
            print(first_name, last_name, email, password)
            customer.password = make_password(customer.password)
            customer.is_active=True
            customer.register()
            current_site = get_current_site(request)
            email_body = {
                    'customer': customer,
                    'domain': current_site.domain,
                    'uid': urlsafe_base64_encode(force_bytes(customer.pk)),
                    'token': account_activation_token.make_token(customer),
                }

            link = reverse('activate', kwargs={
                               'uidb64': email_body['uid'], 'token': email_body['token']})

                

            activate_url = 'http://'+current_site.domain+link
            send_mail(
                'Ecom',
                'Hi '+customer.first_name + ', Please the link below to activate your account \n'+activate_url,
                'from@example.com',
                [email],
                fail_silently=False,)
            return HttpResponse("<h1>An url is sent to your gmail , please click on it to activate your account and then login</h1>")

    else:
            data = {
                'error': error_message,
                'values': value
            }
            return render(request, 'shop/signup.html', data) 


class VerificationView(View):
    def get(self, request, uidb64, token):
        try:
            id = force_text(urlsafe_base64_decode(uidb64))
            customer = Customer.objects.get(pk=id)

            if not account_activation_token.check_token(customer, token):
                return redirect('login'+'?message='+'User already activated')

            if customer.is_active:
                return redirect('login')
            customer.is_active = True
            customer.save()
            messages.success(request, 'Account activated successfully')
            return redirect('login')

        except Exception as ex:
            pass

        return redirect('login')



              


def login(request):
  if request.method=='GET':
        return render(request, 'shop/login.html')
  else:
    
    if request.method=='POST':
        email=request.POST.get('email')
        password=request.POST.get('pass')

        customer = Customer.get_customer_by_email(email)
        error_message = None
        if customer:
            
            flag = check_password(password, customer.password)
            if flag:
                request.session['customer'] = customer.id
                print(request.session['customer'])
                return redirect('ShopHome')
            else:
                error_message = 'Email or Password invalid !!'
        else:
            error_message = 'Email or Password invalid !!'

        print(email, password)
        return render(request, 'shop/login.html', {'error': error_message})  


def signout(request):
 request.session.clear()
 return redirect("ShopHome")

 return HttpResponse('signout')
# Create your views here.

def productView(request, myid):
    product=request.POST.get('product')
    remove=request.POST.get('remove')
    cart=request.session.get('cart')
    if cart:
        quantity=cart.get(product)
        if quantity:
            if remove:
                if quantity==1:
                    cart.pop(product)
                else:
                   cart[product]=quantity-1  
            else:    
                 cart[product]=quantity+1

        else:
         cart[product]=1
    else:
        cart={}
        cart[product]=1
    
    
    request.session['cart']=cart
    print(request.session['cart'])
    

    cart=request.session.get('cart')
    if not cart:
        request.session.cart={}

    
    products=Products.objects.filter(id=myid)
    print(products)

    

    return render(request,'shop/product_detail.html', {'products': products[0]})


def Cart(request):
   
 ids=list(request.session.get('cart').keys())
 ids.remove('null')
 product=Products.objects.filter(id__in=ids)
 print(product)


 ids=list(request.session.get('cart').keys())
 for i in ids:
    if i=='null':
     ids.remove('null')
    elif i=='':
     ids.remove('')
    else:
     product=Products.objects.filter(id__in=ids)
     print(product)

 if len(ids)==0:
     return HttpResponse("<h1>no product on cart add product now</h1>")
     
 return render(request,'shop/cart.html',{'product':product})


def checkout(request):

 ids=list(request.session.get('cart').keys())
 ids.remove('null')
 product=Products.objects.filter(id__in=ids)
 print(product)


 ids=list(request.session.get('cart').keys())
 for i in ids:
    if i=='null':
     ids.remove('null')
    elif i=='':
     ids.remove('')
    else:
     product=Products.objects.filter(id__in=ids)
     print(product)

 cart=request.session.get('cart')
 ids=list(cart.keys())
 for i in ids:
   if i=='null':
     ids.remove('null')
   elif i=='':
     ids.remove('')


     
 if request.method=='POST': 
    address=request.POST.get('address')
    Name=request.POST.get('Name')
    Email=request.POST.get('Email')
    Phone=request.POST.get('Phone')
    country=request.POST.get('country')
    state=request.POST.get('state')
    city=request.POST.get('city')
    Pincode=request.POST.get('Pincode')
    customer=request.session.get('customer')
    cart=request.session.get('cart')
    product=Products.get_products_by_id(ids)

   
    if not Customer.objects.filter(email=Email).exists():
        messages.error(request,"enter the same register email")
        return redirect('checkout')
   
    else:
     print(address,Phone,country,state,city,Pincode,cart,customer,product,Email,Name)

     
     for prod in product:
        print(cart.get(str(prod.id)))
        orders=Orders(Name=Name,Email=Email,customer=Customer(id=customer),address=address,phone=Phone,country=country,state=state,city=city,
               Pincode=Pincode,product=prod,quantity=cart.get(str(prod.id)),price=prod.price*cart.get(str(prod.id)))
        send_mail(
                'Ecom',
                'Your order is placed and is ready for delivery ps: this is just a normal ecom project not a real time online shop website:)',
                'from@example.com',
                [Email],
                fail_silently=False,)       
        orders.placeOrder()
    
     request.session['cart'] = {}
     return redirect("ShopHome") 
 else:
    return render(request,'shop/checkout.html',{'product':product})

@auth_middleware
def order(request):

        customer = request.session.get('customer')
        orders = Orders.get_orders_by_customer(customer)
        print(orders)
        return render(request , 'shop/order.html'  , {'orders' : orders})
