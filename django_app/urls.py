from django.urls import path
from django_app import views


app_name = "django_app"
urlpatterns = [
    path("", views.home, name="home"),
    # path("", views.Home.as_view(), name=""),
    # path("home/", views.Home.as_view(), name="home"),
    #
    # path("user/register/", views.register, name="register"),
    # path("user/login/", views.login_f, name="login"),
    # path("user/logout/", views.logout_f, name="logout"),
    #
    # path("post/create/", views.create, name="create"),
    # path("post/<int:post_id>/detail/", views.read, name="read"),
    # path("post/list/", views.read_list, name="read_list"),
    # path("post/<int:post_id>/update/", views.update, name="update"),
    # path("post/<int:post_id>/delete/", views.delete, name="delete"),
]