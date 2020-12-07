from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class BlogPost(models.Model):

    post_id = models.AutoField
    title = models.CharField(max_length=100)
    head0 = models.CharField(max_length=100)
    cont0 = models.CharField(max_length=1000,default='')
    head1 = models.CharField(max_length=100)
    cont1 = models.CharField(max_length=1000,default='')
    head2 = models.CharField(max_length=100)
    cont2 = models.CharField(max_length=1000,default='')        
    post_date = models.DateField()
    thumbnail = models.ImageField(upload_to='blog/images',default='')

    def __str__(self):
        return self.title