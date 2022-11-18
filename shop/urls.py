from django.urls import path
from . import views

urlpatterns = [
      path('',views.home,name='home' ),
      path('about/',views.about,name='about' ),
      path('contact/',views.contact,name='contact' ),
      path('tracker/',views.tracker,name='tracker' ),
      path('search/',views.search,name='search'),
      path('productview/<int:myid>',views.productview,name='productview'),
      path('checkout/',views.checkout,name='checkout'),
      # path('shop/handlerequest/',views.handlerequest,name='handlerequest'),

      path('login',views.loginUser , name='login'),
      path('create-account',views.signupUser , name='signup'),
      path('logout',views.logoutUser , name='logout')
 ]