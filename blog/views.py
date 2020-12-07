from django.shortcuts import render
from django.http import HttpResponse

from . models import BlogPost

# Create your views here.


def index(request):
    myposts = BlogPost.objects.all()
    params = {'myposts': myposts}
    return render(request, 'blog/index.html',params)


def blogPost(request,id):
    posts = BlogPost.objects.filter(id=id)

    Allposts = [[posts, range(1, 4)]]
    params = {'posts': Allposts}
    return render(request, 'blog/blogPost.html',params)
