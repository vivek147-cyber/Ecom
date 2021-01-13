from django import template

register=template.Library()

@register.filter(name='is_in_cart')
def is_in_cart(product,cart):
  keys=cart.keys()
  for id in keys:  
      if int_or_0(id)==product.id:
          return True
  return False


@register.filter(name='quantity_cart')
def quantity_cart(product,cart):
  keys=cart.keys()
  for id in keys:  
      if int_or_0(id)==product.id:
          return cart.get(id)
  return 0

def int_or_0(value):
    try:
        return int(value)
    except:
        return 0  

@register.filter(name='product_total')
def product_total(product,cart):
 return product.price * quantity_cart(product,cart)


@register.filter(name='cart_price_total')
def cart_price_total(product,cart):
   sum=0 
   for p in product:
     sum=sum+product_total(p, cart)
   return sum


