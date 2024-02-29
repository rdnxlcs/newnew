from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('parkingapp.urls', namespace="parkingapp"))
]
handler404 = 'parkingapp.views.handler404'
handler500 = 'parkingapp.views.handler404'