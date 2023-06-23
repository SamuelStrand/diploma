from django.urls import path
from django_app import views
from django.conf import settings
from django.conf.urls.static import static


app_name = "django_app"

urlpatterns = [
    path("", views.home, name="home"),
    path('post/', views.get_posts, name='get_posts'),
    path('post/create/', views.post_create, name='post_create'),

    path('register/', views.register, name='register'),
    path('login/', views.my_login, name='login'),
    path('logout/', views.my_logout, name='logout'),
]
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
