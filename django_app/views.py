from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import User, update_last_login
from django.core.cache import caches
from django.http import HttpRequest, HttpResponse
from django.shortcuts import render, redirect
from django.urls import reverse

from django_app import models, utils as django_utils
from django_app.forms import ImageForm

DatabaseCache = caches["default"]
LocMemCache = caches["ram_cache"]


def home(request: HttpRequest) -> HttpResponse:
    return render(request, 'home.html')


def register(request: HttpRequest) -> HttpResponse:
    if request.method == "GET":
        context = {}
        return render(request, 'register.html', context=context)

    elif request.method == "POST":
        first_name = request.POST.get('first_name', "")
        last_name = request.POST.get('last_name', "")
        username = request.POST.get('username', None)
        email = request.POST.get('email', None)
        phone_number = request.POST.get('phone_number', None)
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

            if username and password1:
                user_obj = authenticate(username=username, password=password1)
                if user_obj:
                    login(request, user_obj)

            models.Profile.objects.create(
                user=request.user,
                first_name=first_name,
                last_name=last_name,
                email=email,
                phone_number=phone_number,
            )
            return redirect(reverse('django_app:get_posts', args=()))  # name=
        else:
            raise Exception("данные не заполнены!")


def my_login(request: HttpRequest) -> HttpResponse:
    if request.method == 'GET':
        context = {}
        return render(request, 'login.html', context=context)

    if request.method == 'POST':
        username = request.POST.get('username', "")
        password = request.POST.get('password', "")
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


@django_utils.login_required_decorator
def my_logout(request: HttpRequest) -> HttpResponse:
    logout(request)
    return redirect(reverse('django_app:login', args=()))


@django_utils.login_required_decorator
def get_posts(request: HttpRequest) -> HttpResponse:
    post_list = django_utils.caching(
        LocMemCache, f"get_posts django_models.Post.objects.all()", 1,
        lambda: models.Post.objects.all()
    )
    page = django_utils.paginate(request=request, objects=post_list, num_page=6)
    context = {'page': page}
    return render(request, 'posts.html', context=context)


@django_utils.login_required_decorator
def post_create(request: HttpRequest) -> HttpResponse:
    if request.method == 'GET':
        context = {}
        return render(request, 'post_create.html', context=context)

    elif request.method == 'POST':
        form = ImageForm(request.POST, request.FILES)
        form.save()
        image = form.instance

        author = request.user
        title = request.POST.get('title', None)
        description = request.POST.get('description', "")
        price = request.POST.get('price', "")

        if image is None:
            image = 'ads/no_img.jpg'

        if image is not None:
            try:
                models.Post.objects.create(
                    author=author,
                    title=title,
                    description=description,
                    price=price,
                    image=image,
                )
            except:
                return redirect(reverse('django_app:get_posts', args=()))


@django_utils.login_required_decorator
def post_update(request: HttpRequest, post_id: int) -> HttpResponse:
    if request.method == 'GET':
        post = models.Post.objects.get(id=post_id)
        context = {'post': post}
        return render(request, 'post_update.html', context=context)

    elif request.method == 'POST':
        post = models.Post.objects.get(id=post_id)

        form = ImageForm(request.POST, request.FILES)
        form.save()
        image = form.instance

        title = request.POST.get("title", "")
        description = request.POST.get("description", "")
        price = request.POST.get("price", "")

        post.title = title
        post.description = description
        post.description = price
        post.image = image
        try:
            post.save()
        except:
            return redirect(reverse('django_app:read_one', args=(post_id,)))


@django_utils.login_required_decorator
def read_one(request, post_id=None):
    post = django_utils.caching(
        LocMemCache, f"read_one django_models.Post.objects.get(id={post_id})", 1,
        lambda: models.Post.objects.get(id=post_id)
    )
    post_comments = django_utils.caching(
        LocMemCache, f"read_one django_models.PostComment.objects.filter(article=post)", 1,
        lambda: models.PostComment.objects.filter(article=post)
    )
    page = django_utils.paginate(request=request, objects=post_comments, num_page=4)

    context = {"post": post, "page": page}

    return render(request, "post_detail.html", context)


@django_utils.login_required_decorator
def post_delete(request: HttpRequest, post_id: int) -> HttpResponse:
    post = models.Post.objects.get(id=post_id)
    post.delete()
    return redirect(reverse('django_app:get_posts', args=()))


@django_utils.login_required_decorator
def post_like(request: HttpRequest, post_id: int) -> HttpResponse:
    post = models.Post.objects.get(id=post_id)
    post.is_liked = True
    post.save()
    return redirect(reverse('django_app:get_posts', args=()))


@django_utils.login_required_decorator
def post_dislike(request: HttpRequest, post_id: int) -> HttpResponse:
    post = models.Post.objects.get(id=post_id)
    post.is_liked = False
    post.save()
    return redirect(reverse('django_app:get_posts', args=()))


@django_utils.login_required_decorator
def get_liked(request: HttpRequest) -> HttpResponse:
    post_list = django_utils.caching(
        LocMemCache, f"get_liked django_models.Post.objects.all()", 1,
        lambda: models.Post.objects.all()
    )
    context = {'posts': post_list}
    return render(request, 'post_like.html', context=context)


@django_utils.login_required_decorator
def profile(request: HttpRequest) -> HttpResponse:
    posts = django_utils.caching(
        LocMemCache, f"profile django_models.Post.objects.all()", 1,
        lambda: models.Post.objects.all()
    )
    page = django_utils.paginate(request=request, objects=posts, num_page=2)

    profile_comments = django_utils.caching(
        LocMemCache, f"profile django_models.ProfileComment.objects.all()", 1,
        lambda: models.ProfileComment.objects.all()
    )
    page2 = django_utils.paginate(request=request, objects=profile_comments, num_page=2)
    context = {'page': page, 'page2': page2, 'profile_comments': profile_comments}
    return render(request, 'profile.html', context=context)


@django_utils.login_required_decorator
def post_comment_create(request: HttpRequest, post_id: int) -> HttpResponse:
    if request.method == 'POST':
        text = request.POST.get('text', None)
        post = models.Post.objects.get(id=post_id)
        models.PostComment.objects.create(
            user=request.user,
            article=post,
            text=text
        )

        return redirect(reverse('django_app:read_one', args=(post_id,)))


@django_utils.login_required_decorator
def post_comment_delete(request: HttpRequest, post_id: int) -> HttpResponse:
    comment = models.PostComment.objects.get(id=post_id)
    post_id = comment.article.id
    comment.delete()
    return redirect(reverse('django_app:read_one', args=(post_id,)))


@django_utils.login_required_decorator
def complaint(request: HttpRequest, post_id: int) -> HttpResponse:
    post = django_utils.caching(
        LocMemCache, f"complaint django_models.Post.objects.get(id={post_id})", 1,
        lambda: models.Post.objects.get(id=post_id)
    )

    context = {'post': post}

    if request.method == 'GET':
        return render(request, 'post_complaint.html', context=context)

    if request.method == 'POST':
        reason = request.POST.get('reason', None)
        post = models.Post.objects.get(id=post_id)
        models.Complaint.objects.create(
            user=request.user,
            post=post,
            reason=reason
        )
        return redirect(reverse('django_app:get_posts', args=()), context=context)


@django_utils.login_required_decorator
def get_profiles(request: HttpRequest) -> HttpResponse:
    profile_list = django_utils.caching(
        LocMemCache, f"get_posts django_models.Profile.objects.all()", 1,
        lambda: models.Profile.objects.all()
    )
    page = django_utils.paginate(request=request, objects=profile_list, num_page=3)
    context = {'page': page}
    return render(request, 'all_profiles.html', context=context)


@django_utils.login_required_decorator
def detail_profile(request, profile_id=None):
    user_profile = django_utils.caching(
        LocMemCache, f"detail_profile django_models.Profile.objects.get(id={profile_id})", 1,
        lambda: models.Profile.objects.get(id=profile_id)
    )
    profile_comments = django_utils.caching(
        LocMemCache, f"detail_profile django_models.ProfileComment.objects.filter(article=post)", 1,
        lambda: models.ProfileComment.objects.filter(profile=user_profile)
    )
    page = django_utils.paginate(request=request, objects=profile_comments, num_page=2)

    posts = django_utils.caching(
        LocMemCache, f"profile django_models.Post.objects.all()", 1,
        lambda: models.Post.objects.all()
    )

    posts = posts[:2]

    context = {"user_profile": user_profile, "profile_comments": page, 'posts': posts}

    return render(request, "detail_profile.html", context)


@django_utils.login_required_decorator
def profile_comment_create(request: HttpRequest, profile_id: int) -> HttpResponse:
    if request.method == 'POST':
        text = request.POST.get('text', None)
        my_profile = models.Profile.objects.get(id=profile_id)
        models.ProfileComment.objects.create(
            user=request.user,
            profile=my_profile,
            text=text
        )

        return redirect(reverse('django_app:detail_profile', args=(profile_id,)))
