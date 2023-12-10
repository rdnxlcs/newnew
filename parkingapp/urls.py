from django.urls import path
from . import views

app_name="parkingapp"

urlpatterns = [
    path('index', views.index, name='index'),
    path('sign', views.sign, name='sign'),
    path('enter', views.enter, name='enter'),
    path('panel', views.panel, name='panel'),
    path('addparking', views.addparking, name='addparking'),
    path('signadmin', views.signadmin, name='signadmin'),
    path('signcoupon', views.signcoupon, name='signcoupon'),
    path('coupon', views.coupon, name='coupon'),
    path('endparking', views.endparking, name='endparking'),
    path('esp', views.esp, name='esp'),
    path('error', views.error, name='error'),
]