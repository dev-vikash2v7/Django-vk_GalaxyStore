from django.db import models

class Category(models.Model):
    name = models.CharField(max_length=50)
    sub_category = models.ManyToManyField("SubCategory" , blank = True  ,  related_name = 'sub_category')

    def __str__(self):
        return self.name

    

class SubCategory(models.Model):
    name = models.CharField(max_length=50 , default='')
    products =  models.ManyToManyField("Product" , blank = True  ,  related_name = 'products')

  
    def __str__(self):
        return self.name


class Product(models.Model):
    name = models.CharField(max_length=100 , default='')
    price = models.IntegerField(default=0)
    description = models.TextField(max_length=500 , default='')
    brand = models.CharField(max_length=50 , default = 'india')
    color = models.CharField(max_length=20 , default = 'black')
    size = models.CharField(max_length=10 , default = '-')

    category = models.ForeignKey(Category  ,blank=True , on_delete=models.CASCADE )
    sub_category = models.ForeignKey(SubCategory  ,blank=True , on_delete=models.CASCADE   )


    image = models.ImageField(upload_to='shop/images' )

    def __str__(self):
        return self.name

    def get_products_by_category( category):
         return Product.objects.filter(category__name=category)


class User(models.Model):
    name = models.CharField(max_length=50 , default='')
    email = models.CharField(max_length=50,default='')
    city = models.CharField(max_length=10,default='')
    # phone = models.IntegerField(default=0)
    # address = models.CharField(max_length=100)
    # state = models.CharField(max_length=10,default='')
    # zip = models.IntegerField(default=0)

    def __str__(self):
        return self.name


class Order(models.Model):
    created_on = models.DateTimeField(auto_now_add = True)
    amount = models.IntegerField(default=0)
    is_paid = models.BooleanField(default = False)

    products = models.ManyToManyField('Product' , blank = True) 
    user = models.OneToOneField('User' , on_delete=models.CASCADE ) 

    def __str__(self) -> str:
        return f'Order: {self.created_on.strftime("%b %d %I: %M %p")}'# Nov 04 04: 13 PM



class Tracker(models.Model):
    is_shipped = models.BooleanField(default=False)
    order =   models.OneToOneField(Order , on_delete=models.CASCADE)
    trackerUpdate_desc = models.TextField(max_length=5000)
    timeStamp = models.DateField(auto_now_add=True)

    def __str__(self):
        return self.trackerUpdate_desc[0:7] + '...'