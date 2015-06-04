from django.conf.urls import patterns
from django.conf.urls import url

from openstack_dashboard.dashboards.nfv.vnfcatalog import views


urlpatterns = patterns(
    'openstack_dashboard.dashboards.nfv.vnfcatalog.views',
    url(r'^$', views.IndexView.as_view(), name='index'),
    url(r'^onboardvnf', views.OnBoardVNFView.as_view(), name='onboardvnf'),
)
