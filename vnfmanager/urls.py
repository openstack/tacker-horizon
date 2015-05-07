from django.conf.urls import patterns
from django.conf.urls import url

from openstack_dashboard.dashboards.nfv.vnfmanager import views


urlpatterns = patterns(
    'openstack_dashboard.dashboards.nfv.vnfmanager.views',
    url(r'^$', views.IndexView.as_view(), name='index'),
    url(r'^addservice$', views.AddServiceView.as_view(), name='addservice'),
)
