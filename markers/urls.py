
from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
         path('', views.home,name='index'),
        #  ''' path('bargraph', views.bargraph),     '''    # path('Graph.png$', views.displaygraph),
]
