from django.urls import path

# from django.conf.urls import url
from . import views

urlpatterns = [
    path("request/verify/code/<str:phone>/<str:uuid>", views.requestCode),
    path("fetch", views.fetchData),
]
