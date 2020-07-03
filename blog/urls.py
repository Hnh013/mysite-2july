from django.conf.urls import url
from . import views
from django.contrib.auth.views import LoginView

urlpatterns = [   
    # url(r'^login/$', auth_views.LoginView.as_view(), name='login'),
    # url(r'^logout/$', auth_views.logout, name='logout'),
    url(r'^recharge/$', views.recharge, name='recharge'),
    url(r'^charge/$', views.charge, name='charge'),
    #url(r'^success/<str:args>$', views.successMsg, name='success'),
    url(r'^$', views.index, name='index'),
    url(r'^home/$', views.home, name='home'),
    url(r'^signup/$', views.signup, name='signup'),
    url(r'^activate/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$',
        views.activate, name='activate'),
    url(r'^confirmed_account/', views.confirmed_account, name='confirmed_account'),
]