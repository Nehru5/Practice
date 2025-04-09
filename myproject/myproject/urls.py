from django.contrib import admin
from django.urls import path
from myapp.views import Login_, Signup, Session_Example, Session_Get, Flush

urlpatterns = [
    path('admin/', admin.site.urls),
    path("",Signup, name="signup"),
    path("login/", Login_, name="login"),
    path("hi/", Session_Example, name="hi"),
    path("get/", Session_Get, name = "get"),
    path("delete/", Flush, name="delete")
]
handler404 = 'myapp.views.custom_404_view'

