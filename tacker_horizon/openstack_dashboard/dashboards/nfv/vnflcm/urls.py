# Copyright (C) 2024 Fujitsu
# All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License"); you may
# not use this file except in compliance with the License. You may obtain
# a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
# WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
# License for the specific language governing permissions and limitations
# under the License.


from django.urls import re_path

from tacker_horizon.openstack_dashboard.dashboards.nfv.vnflcm \
    import views

urlpatterns = [
    re_path(r'^$', views.IndexView.as_view(), name='index'),
    re_path(r'^(?P<id>[^/]+)/$', views.DetailView.as_view(), name='detail'),
    re_path(r'^createvnfidentifier$', views.CreateVnfIdentifierView.as_view(),
            name='createvnfidentifier'),
    re_path(r'^(?P<id>[^/]+)/instantiatevnf/$',
            views.InstantiateVnfView.as_view(),
            name='instantiatevnf'),
    re_path(r'^(?P<id>[^/]+)/terminatevnf/$', views.TerminateVnfView.as_view(),
            name='terminatevnf'),
    re_path(r'^(?P<id>[^/]+)/healvnf/$', views.HealVnfView.as_view(),
            name='healvnf'),
    re_path(r'^(?P<id>[^/]+)/updatevnf/$', views.UpdateVnfView.as_view(),
            name='updatevnf'),
    re_path(r'^(?P<id>[^/]+)/scalevnf/$', views.ScaleVnfView.as_view(),
            name='scalevnf'),
    re_path(r'^(?P<id>[^/]+)/changeconnectivity/$',
            views.ChangeExternalVnfConnectivityView.as_view(),
            name='changeconnectivity'),
    re_path(r'^(?P<id>[^/]+)/changevnfpkg/$',
            views.ChangeCurrentVnfPackageView.as_view(),
            name='changevnfpkg'),
]
