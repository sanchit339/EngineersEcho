from django.shortcuts import render
from django.http import HttpResponse

from .models import Post

# Create your views here.
def home(request):
    # we have to pass dictionary here
    context = {
        'posts': Post.objects.all(),
    }
    return render(request, "blog/home.html" , context)


def about(request):
    return render(request, 'blog/about.html' , {'title': "About Page"})
