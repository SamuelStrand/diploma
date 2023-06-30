from django.urls import path
from django_app import views
from django.conf import settings
from django.conf.urls.static import static

app_name = "django_app"

urlpatterns = [
    path("", views.home, name="home"),

    path('post/', views.get_posts, name='get_posts'),
    path('post/create/', views.post_create, name='post_create'),
    path("post/<int:post_id>/detail/", views.read_one, name="read_one"),
    path('post/<int:post_id>/update/', views.post_update, name='post_update'),
    path('post/<int:post_id>/delete/', views.post_delete, name='post_delete'),

    path('post/<int:post_id>/liked_posts/', views.post_like, name='post_like'),
    path('post/<int:post_id>/disliked_posts/', views.post_dislike, name='post_dislike'),

    path('post/<int:post_id>/complaint/create', views.complaint, name='complaint'),

    path('post/liked', views.get_liked, name='get_liked'),

    path('register/', views.register, name='register'),
    path('login/', views.my_login, name='login'),
    path('logout/', views.my_logout, name='logout'),

    path('my_profile/', views.profile, name='profile'),
    path('profiles/', views.get_profiles, name='get_profiles'),
    path("profiles/<int:profile_id>/detail/", views.detail_profile, name="detail_profile"),

    path('post/<int:post_id>/comment/create/', views.post_comment_create, name='post_comment_create'),
    path('post/<int:post_id>/comment/delete/', views.post_comment_delete, name='post_comment_delete'),

    path('profile/<int:profile_id>/comment/create/', views.profile_comment_create, name='profile_comment_create'),

]
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
