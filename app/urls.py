from django.conf.urls import include, url
from . import views

urlpatterns = [
    url(r'^home/', views.home),
    url(r'^generateKeys/', views.generateKeys),
    url(r'^generate2/', views.generate2),
    url(r'^verify/', views.verify),
    url(r'^vote/', views.vote),
    url(r'^final/', views.final),
]