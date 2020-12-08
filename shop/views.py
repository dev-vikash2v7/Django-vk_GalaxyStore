from django.shortcuts import render, redirect
from django.http import HttpResponse

from .models import Product, Contact, Order, Tracker
from math import ceil
import json

# for login and logout
from django.contrib.auth.models import User
from django.contrib.auth import logout, authenticate, login

# for payment
from Paytm import Checksum
from django.views.decorators.csrf import csrf_exempt
MERCHANT_KEY = 'kbzk1DSbJiV_O3p5'


# Create your views here.
def home(request):
    print(request.user)

    # if request.user.is_anonymous:
    #    return redirect('/login')

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
        return render(request, 'shop/contact.html', {'submit': True, 'name': name})

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
        amount = request.POST.get('amount', ' ')
        
        name = request.POST.get('name', ' ')
        phone = request.POST.get('phone', ' ')
        email = request.POST.get('email', ' ')
        address = request.POST.get('add1', ' ')
        city = request.POST.get('city', ' ')
        state = request.POST.get('state', ' ')
        zip = request.POST.get('zip', ' ')

        order_comp = True
        params = {'order_comp': order_comp}

        order = Order(order_list=order_list, name=name, phone=phone, email=email,
                      address=address, city=city, state=state, zip=zip,amount=amount)
        order.save()
        order_comp = True
        id = order.order_id

        tracker_id = Tracker(
            order_id=id, trackerUpdate_desc='Your Order reach to Chickdhaliya . 10 min mein phunch jaega ... thoda dheeraj rkho. :)')
        tracker_id.save()

        params = {'order_comp': order_comp, 'order_id': id,
                  'name': name, 'address': address}

        # return render(request, 'shop/checkout.html', params)
        
        data_dict = {
            'MID': 'WorldP64425807474247',
            'ORDER_ID': str(order.order_id*10),
            'TXN_AMOUNT': str(amount),
            'CUST_ID': email,
            'INDUSTRY_TYPE_ID': 'Retail',
            'WEBSITE': 'WEBSTAGING',
            'CHANNEL_ID': 'WEB',
            'CALLBACK_URL': 'http://127.0.0.1:8000/shop/handlerequest/',
        }
        print('data_dict = ',data_dict)
        data_dict['CHECKSUMHASH'] = Checksum.generate_checksum(
            data_dict, MERCHANT_KEY)

        # request paytm to send amount here after user comp
        return render(request, 'shop/paytm.html', {'data_dict': data_dict})

    return render(request, 'shop/checkout.html')

# for payment with paytm
@csrf_exempt
def handlerequest(request):
    # paytm sent post request here
    form = request.POST
    response_dict = {}

    for i in form.keys():
        response_dict[i] = form[i]
        if i == 'CHECKSUMHASH':
            checksum = form[i]

    verify = Checksum.verify_checksum(response_dict,MERCHANT_KEY,checksum)
    print('verify :',verify)
    print('response dict := ',response_dict)
    if verify:
        if response_dict['RESPCODE'] == '01':
            print('Payment Successfull')
        else:
            print('paument was not successfull because',
                  response_dict['RESPMSG'])
    else:
        print('paument was not successfull because', response_dict['RESPMSG'])
    return render( request , 'shop/paymentStatus.html',{'response':response_dict} )








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

                    updates.append(
                        {'desc': item.trackerUpdate_desc, 'time': item.timeStamp})
                    # print('updates :', updates)
                    # updates : [{'desc': 'coming soon', 'time': datetime.date(2020, 11, 30)}]

                    response = json.dumps(
                        [updates, order[0].order_list], default=str)
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
