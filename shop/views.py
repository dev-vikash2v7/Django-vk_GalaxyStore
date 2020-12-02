from django.shortcuts import render, redirect
from django.http import HttpResponse

from .models import Product, Contact, Order, Tracker
from math import ceil
import json

# for login and logout
from django.contrib.auth.models import User
from django.contrib.auth import logout, authenticate, login


# Create your views here.
def home(request):
    print(request.user)

    if request.user.is_anonymous:
        return redirect('/login')

    products = Product.objects.all()

    n = len(products)

    if n % 4 == 0:
        nSlide = n/4
    else:
        nSlide = ceil(n//4) + 1

    # nSlide = n//4 + ceil( (n/4) - (n//4) )

    allProds = []
    catProds = Product.objects.values('category')

    # cats = { item['category'] for item in catProds }

    # apna logic
    cats = set()
    for item in catProds:
        for key, value in item.items():
            if key == 'category':
                cats.add(value)

    for cat in cats:

        prod = Product.objects.filter(category=cat)
        allProds.append([prod, range(1, nSlide), nSlide])

    params = {'allProds': allProds}

    return render(request, 'shop/home.html', params)


def about(request):
    return render(request, 'shop/about.html')


def contact(request):
    if request.method == 'POST':
        name = request.POST.get('name', ' ')
        phone = request.POST.get('phone', ' ')
        email = request.POST.get('email', ' ')
        subject = request.POST.get('subject', ' ')
        message = request.POST.get('massage', ' ')

        contact = Contact(name=name, phone=phone, email=email,
                          subject=subject, message=message)
        contact.save()
    return render(request, 'shop/contact.html')


def search(request):
    return render(request, 'shop/search.html')


def productview(request, myid):
    product_id = Product.objects.filter(id=myid)
    params = {'product': product_id[0]}
    return render(request, 'shop/productview.html', params)


def checkout(request):
    if request.method == 'POST':

        order_list = request.POST.get('order_list', ' ')

        name = request.POST.get('name', ' ')
        phone = request.POST.get('phone', ' ')
        email = request.POST.get('email', ' ')
        add1 = request.POST.get('add1', ' ')
        add2 = request.POST.get('add2', ' ')
        city = request.POST.get('city', ' ')
        state = request.POST.get('state', ' ')
        zip = request.POST.get('zip', ' ')

        order_comp = True
        params = {'order_comp': order_comp}

        order = Order(order_list=order_list, name=name, phone=phone, email=email,
                      address=add1 + ' '+add2, city=city, state=state, zip=zip)
        order.save()
        order_comp = True
        id = order.order_id

        tracker_id = Tracker(
            order_id=id, trackerUpdate_desc='Your Order reach to Chickdhaliya . 10 min mein phunch jaega ... thoda dheeraj rkho. :)')
        tracker_id.save()

        params = {'order_comp': order_comp, 'order_id': id, 'name': name}

        return render(request, 'shop/checkout.html', params)
    return render(request, 'shop/checkout.html')

# track the order


def tracker(request):
    print('In tracker func')
    if request.method == 'POST':
        OrderId = request.POST.get('OrderId')
        email = request.POST.get('email', ' ')

        try:
            order = Order.objects.filter(order_id=OrderId, email=email)
            print('order', order)
            # <QuerySet [<Order: vikash verma v@gmail.com>]>

            if len(order) > 0:

                tracker_update = Tracker.objects.filter(order_id=OrderId)
                # print('tracker list :', tracker_update)
                # tracker list : <QuerySet [<Tracker: Your Or...>, <Tracker: come at...>]>

                updates = []

                for item in tracker_update:
                    # print('item :', item)
                    # item : come at...

                    updates.append( {'desc': item.trackerUpdate_desc, 'time': item.timeStamp}   )
                    # print('updates :', updates)
                    # updates : [{'desc': 'coming soon', 'time': datetime.date(2020, 11, 30)}]

                    response = json.dumps([updates, order[0].order_list ], default=str)
                    # print('response : ', response, order[0])
                    # response :  [[{"desc": "Your Order reach to Chickdhaliya . 10 min mein phunch jaega ... thoda dheeraj rkho. :)", "time": "2020-12-02"}, {"desc": "come at bus stop of punasa", "time": "2020-12-02"}], "{"{\"pr7\":[3,\"printer\"],\"pr8\":[3,\"bluetooth\"]}"] vikash v@gmail.com

                    print(order[0].order_list) 
                    # {"pr7":[3,"printer"],"pr8":[3,"bluetooth"]}
                    # print(order[0])# <class 'shop.models.Order'>

                return HttpResponse(response)

            else:
                print('user not found')
                return HttpResponse('{}')

        except Exception as e:
            print('error :', e)
            return HttpResponse('{}')

    return render(request, 'shop/tracker.html')


def loginUser(request):
    if request.method == 'POST':

        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')

        # ceheck if user has corect authanticate
        user = authenticate(username=username, email=email, password=password)

        if user is not None:
            login(request, user)
            # a backend authenticate the credentials
            return redirect('/')

        else:
            # no backend authenticte the credentials
            return render(request, 'login/login.html')

    return render(request, 'login/login.html')


def logoutUser(request):
    logout(request)
    return redirect('/login')
