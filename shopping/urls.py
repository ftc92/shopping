from django.contrib import admin
from django.urls import path
from django.conf.urls import url,include
from register import views
from search import views as search

urlpatterns = [
    path('admin/', admin.site.urls),
    url(r'^$',search.index,name='index'),
    url(r'^register/',include('register.urls')),
    url(r'^logout/$', views.user_logout, name='logout'),
]