from django.urls import path
from . import views

app_name="parkingapp"

urlpatterns = [
    path('', views.index, name='index'),
    path('logout/', views.logout, name='logout'),
    path('dont_have_access/', views.dont_have_access, name='dont_have_access'),
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