from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

from recipeapp.views import home

urlpatterns = [
  path('',home,name='home')
]
