from django.urls import path
from . import views

urlpatterns = [
    path('',views.index,name='blog-index'),
    path('blogpost/<int:id>',views.blogPost,name = 'blog_post')
]