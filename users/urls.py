"""
URL configuration for EngineersEcho project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.urls import path
from . import views as user_view
from django.contrib.auth import views as auth_view

urlpatterns = [
    path('register/', user_view.register, name='register'),
    path('login/', auth_view.LoginView.as_view(template_name='users/login.html'), name='login'),
    path('logout/', auth_view.LogoutView.as_view(template_name="users/logout.html"), name='users-logout' ),

    path('profile/', user_view.profile, name='profile'),
    # django dispatcher concept. i.e, passing info through the url.
    path('profile/<data>', user_view.another_user_profile, name="another_user-profile"),
    path('profile/<data>/<int:pageno>', user_view.another_user_profile, name="another_user_profilee"),

    path('search_user/', user_view.search_user, name="search_user"),
]
