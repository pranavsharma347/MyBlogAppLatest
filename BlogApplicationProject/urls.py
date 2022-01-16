"""BlogApplicationProject URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
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
from django.contrib import admin
from django.urls import path,include
from BlogApp import views
from django.views.generic import TemplateView
from django.contrib.auth import views as auth_views
admin.site.site_header="MyBlogApp Admin"
admin.site.site_title="MyBlogApp"
admin.site.index_title="Welcome to MyBlogAdmin Panel"
urlpatterns = [
    path('admin/', admin.site.urls),
    path('contactus/',views.contactus,name='contactus'),
    path('home/',views.home,name='home'),
    path('blog/',views.blog),
    # path('latestpost/',views.latestpost,name='latestpost'),
    path('blogpost/<slug:slug>/',views.blogpost,name='blogpost'),
    path('searchpost/',views.searchpost,name='searchpost'),
    path('logout/',views.userlogout,name='logout'),
    path('blogComment/',views.blogComment,name='blogComment'),
    path('loginlogout/',views.baseloginlogout),
    path('basesignup/',views.basesignup,name='basesignup'),
    path('',views.baselogin,name='baselogin'),
    path('sharebymail/',views.sharebymail,name='sharebymail'),
    # path('accounts/', include('allauth.urls')),

    path('social-auth/', include('social_django.urls', namespace="social")),# add for social_django_auth
    # path('accounts/', include('django.contrib.auth.urls'))
    path('password_reset/',auth_views.PasswordResetView.as_view(template_name='BlogApp/password_reset.html'),name='password_reset'),
    #here password_reset is my own customize template
    path('password_reset_done/',auth_views.PasswordResetDoneView.as_view(template_name='BlogApp/password_reset_done.html'),name='password_reset_done'),
    path('password_reset_confirm/<uidb64>/<token>/',auth_views.PasswordResetConfirmView.as_view(template_name='BlogApp/password_reset_confirm.html'),name="password_reset_confirm"),
    path('password_reset_complete/',auth_views.PasswordResetCompleteView.as_view(template_name='BlogApp/password_reset_complete.html'),name="password_reset_complete"),
    #here PasswordResetView is an built in class django-admin
    #if you use password resset of django admin then PasswordResetView,PasswordResetDoneView,PasswordResetConfirmView,PasswordResetCompleteView compulsory required
    path('activate/<uidb64>/<token>/',views.activate,name='activate'),
    path('changepassword/',views.changePassword,name='changepassword')



]