
from django.contrib import admin
from django.urls import path, include
from .views import loginfunc, signupfunc, topfunc, logoutfunc, BlogCreate, BlogDelete

urlpatterns = [
    path('', topfunc, name=''),
    path('login', loginfunc, name='login'),
    path('logout/', logoutfunc, name='logout'),
    path('signup/', signupfunc, name='signup'),
    path('top/', topfunc, name='top'),
    path('delete/<int:pk>', BlogDelete.as_view(), name='delete'),
    path('create/', BlogCreate.as_view(), name='create'),
] 
