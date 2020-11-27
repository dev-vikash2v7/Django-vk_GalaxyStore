from django.shortcuts import render,redirect
from django.http import HttpResponse

from .models import Product,Contact
from math import ceil

# for login and logout
from django.contrib.auth.models import User
from django.contrib.auth import logout,authenticate,login


# Create your views here.
def home(request):
    print(request.user)

    if request.user.is_anonymous:
        return redirect('/login')

    products = Product.objects.all()

    n = len(products)
    
    if n%4 == 0:
        nSlide = n/4
    else:
        nSlide = ceil(n//4 ) + 1 


    # nSlide = n//4 + ceil( (n/4) - (n//4) )

    allProds = []
    catProds = Product.objects.values('category')

    # cats = { item['category'] for item in catProds }

    # apna logic
    cats = set()
    for item in catProds:
        for key,value in item.items():
            if key == 'category': 
                cats.add(value)

    

    for cat in cats:
    
        prod = Product.objects.filter(category = cat)
        allProds.append([ prod , range(1, nSlide) , nSlide ])

    params = {'allProds' : allProds}

    return render(request,'shop/home.html',params)


def about(request):
    return render(request,'shop/about.html')

def contact(request):
    if request.method == 'POST':
        name = request.POST.get('name',' ')
        phone = request.POST.get('phone',' ')
        email = request.POST.get('email',' ')
        subject =request.POST.get('subject',' ')
        message =request.POST.get('massage',' ')
        
        contact = Contact(name=name , phone=phone ,email=email ,subject=subject , message=message)
        contact.save()
    return render(request,'shop/contact.html')

def tracker(request):
    return render(request,'shop/tracker.html')

def search(request):
    return render(request,'shop/search.html')

def productview(request, myid):
    product_id = Product.objects.filter(id=myid)
    params = {'product' : product_id[0]}
    return render(request,'shop/productview.html',params)

def checkout(request):
   return render(request,'shop/checkout.html')

def loginUser(request):
    if request.method == 'POST':

        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')

        print(username,password)

        # ceheck if user has corect authanticate
        user = authenticate(username=username , email = email ,password = password)

        if user is not None:
            login(request,user)
            # a backend authenticate the credentials
            return redirect('/')

        else:
            # no backend authenticte the credentials
            return render(request,'login/login.html')


    return render(request,'login/login.html')

def logoutUser(request):
    logout(request)
    return redirect('/login')




