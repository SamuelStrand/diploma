from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import User, update_last_login
from django.http import HttpRequest, HttpResponse
from django.shortcuts import render, redirect
from django.urls import reverse

from django_app import models
from django_app.forms import ImageForm


# Create your views here.
def home(request: HttpRequest) -> HttpResponse:
    context = {}
    return render(request, 'home.html', context=context)


def get_posts(request: HttpRequest) -> HttpResponse:
    posts = models.Post.objects.all()
    context = {'posts': posts}
    return render(request, 'posts.html', context=context)


def register(request: HttpRequest) -> HttpResponse:
    if request.method == "GET":
        context = {}
        return render(request, 'register.html', context=context)

    elif request.method == "POST":
        first_name = request.POST.get('first_name', "")
        last_name = request.POST.get('last_name', "")
        username = request.POST.get('username', None)
        password1 = request.POST.get('password1', "")
        password2 = request.POST.get('password2', "")

        if password1 and password1 != password2:
            raise Exception("пароли не совпадают!")
        if username and password1:
            User.objects.create(
                first_name=first_name,
                last_name=last_name,
                username=username,
                password=make_password(password1),
            )
            return redirect(reverse('django_app:login', args=()))  # name=
        else:
            raise Exception("данные не заполнены!")


def my_login(request: HttpRequest) -> HttpResponse:
    if request.method == 'GET':
        context = {}
        return render(request, 'login.html', context=context)

    if request.method == 'POST':
        username = request.POST.get('username', "")
        password = request.POST.get('password', "")
        print(username)
        print(password)
        if username and password:
            user_obj = authenticate(username=username, password=password)
            if user_obj:
                login(request, user_obj)
                update_last_login(sender=None, user=user_obj)
                return redirect(reverse('django_app:get_posts', args=()))
            else:
                raise Exception('данные не совпадают')
        else:
            raise Exception('no data')


def my_logout(request: HttpRequest) -> HttpResponse:
    logout(request)
    return redirect(reverse('django_app:login', args=()))


def post_create(request: HttpRequest) -> HttpResponse:
    if request.method == 'GET':
        context = {}
        return render(request, 'post_create.html', context=context)
    elif request.method == 'POST':
        form = ImageForm(request.POST, request.FILES)
        form.save()
        image = form.instance
        title = request.POST.get('title', None)
        description = request.POST.get('description', "")
        price = request.POST.get('price', "")

        try:
            models.Post.objects.create(
                author=request.user,
                title=title,
                description=description,
                price=price,
                image=image,
            )
        except:
            return redirect(reverse('django_app:get_posts', args=()))
