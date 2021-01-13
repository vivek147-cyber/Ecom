
from django.urls import path
from django.contrib.auth import views as auth_views
from .import views
from shop.views import VerificationView


urlpatterns = [
    path("",views.index,name="ShopHome"),
    path("about/", views.about, name="about"),
    path("contact/",views.contact,name="contact"),
    path("categories/",views.categories,name="categories"),
    path("signup/",views.signup,name="signup"),
    path("login/",views.login,name="login"),
    path("signout/",views.signout,name="signout"),
    path("Cart/",views.Cart,name="Cart"),
    path("order/",views.order,name="order"),
    path("checkout/",views.checkout,name="checkout"),
    path("products/<int:myid>", views.productView, name="ProductView"),
    path('activate/<uidb64>/<token>',VerificationView.as_view(), name='activate'),
    
]