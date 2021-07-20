#bruker mest denne

from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name="hjem"),
    path('about', views.about, name="about"),
]
