from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^profile/$',views.profile, name='profile'),
    url(r'^input/$',views.input, name='input'),
    url(r'^arduino/$',views.arduino, name='arduino'),
    url(r'^result/$',views.result, name='result'),
]