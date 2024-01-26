from django.urls import path
from . import views

app_name="parkingapp"

urlpatterns = [
    path('', views.index, name='index'),
    path('logout/', views.logout, name='logout'),
    path('dont_have_access/', views.dont_have_access, name='dont_have_access'),
    path('sign/', views.sign, name='sign'),
    path('enter/', views.enter, name='enter'),
    path('addparking/', views.addparking, name='addparking'),
    path('signadmin/', views.signadmin, name='signadmin'),
    path('signcoupon/', views.signcoupon, name='signcoupon'),
    path('coupon/', views.coupon, name='coupon'),
    path('endparking/', views.endparking, name='endparking'),
    path('esp/', views.esp, name='esp'),
    path('error/', views.error, name='error'),
    path('charts/', views.compare_time, name='charts'),
    path('dash_full/', views.dash_full, name='dash_full'),
    path('dash_fin/', views.dash_fin, name='dash_fin'),
    path('dash_users/', views.dash_users, name='dash_users'),
    path('dash_parks/', views.dash_parks, name='dash_parks'),
    path('dash_reciepts/', views.dash_reciepts, name='dash_reciepts'),
    path('parkings/', views.parkings, name='parkings'),
]