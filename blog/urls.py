from django.conf.urls import url
from . import views
#from django.contrib.auth.views import views as auth_views

urlpatterns = [   
    #url(r'^login/$', auth_views.LoginView.as_view(), name='login'),
    #url(r'^logout/$', auth_views.logout, name='logout'),
    url(r'^signup/$', views.signup, name='signup'),
    url(r'^activate/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$',
        views.activate, name='activate'),
    url(r'^accouont/<str:pro>', views.account, name='account')
]