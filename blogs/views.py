from django.http import HttpResponse
from django.shortcuts import render

# Create your views here.


def index(request):
    return render(request, 'blogs/index.html')


def posts(request):
    return HttpResponse('posts')


def post_detail(request, slug):
    return HttpResponse('post by id: ' + slug)
