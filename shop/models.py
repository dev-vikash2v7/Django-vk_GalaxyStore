from django.db import models

# Create your models here.

class Product(models.Model):

    prod_id = models.AutoField
    prod_name = models.CharField(max_length=50)
    prod_price = models.IntegerField(default=0)
    category = models.CharField(max_length=50,default='')
    sub_category = models.CharField(max_length=50,default='')
    desc = models.CharField(max_length=200,default='')
    prod_date = models.DateField()
    prod_image = models.ImageField(upload_to='shop/images',default='')

    def __str__(self):
        return self.prod_name

class Contact(models.Model):

    contact_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=50)
    phone = models.IntegerField(default=0)
    email = models.CharField(max_length=50,default='')
    subject = models.CharField(max_length=50,default='')
    message = models.CharField(max_length=200,default='')

    def __str__(self):
        return self.name

class Order(models.Model):

    order_id = models.AutoField(primary_key=True)
    order_list = models.CharField(max_length=200)
    name = models.CharField(max_length=50)
    phone = models.IntegerField(default=0)
    email = models.CharField(max_length=50,default='')
    address = models.CharField(max_length=100)
    city = models.CharField(max_length=10,default='')
    state = models.CharField(max_length=10,default='')
    zip = models.IntegerField(default=0)


    def __str__(self):
        return self.name + ' '+ self.email

class Tracker(models.Model):

    tracker_id = models.AutoField(primary_key=True)
    order_id = models.IntegerField(default=0)
    trackerUpdate_desc = models.CharField(max_length=5000)
    timeStamp = models.DateField(auto_now_add=True)

    def __str__(self):
        return self.trackerUpdate_desc[0:7] + '...'
    
