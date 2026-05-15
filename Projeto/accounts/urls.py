from django.urls import path
from . import views

urlpatterns = [
    path("login/", views.login_view, name="login"),
    path("logout/", views.logout_view, name="logout"),
    path("registo/", views.registo_view, name="registo"),
    path("magic-link/", views.enviar_magic_link, name="pedir_magic_link"),
    path("magic-login/<str:token>/", views.magic_login, name="magic_login"),
]
