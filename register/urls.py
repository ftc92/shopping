# register/urls.py
from register import views
from django.conf.urls import url

# SET THE NAMESPACE!
app_name = 'register'
urlpatterns=[
    url(r'^register/$',views.register,name='register'),
    url(r'^user_login/$',views.user_login,name='user_login'),
]