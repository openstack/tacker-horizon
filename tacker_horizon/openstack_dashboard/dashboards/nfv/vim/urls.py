# Copyright 2016 Brocade Communications System, Inc.
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

from tacker_horizon.openstack_dashboard.dashboards.nfv.vim import views

urlpatterns = [
    re_path(r'^$', views.IndexView.as_view(), name='index'),
    re_path(r'^registervim$', views.RegisterVIMView.as_view(),
            name='registervim'),
    re_path(r'^(?P<vim_id>[^/]+)/$', views.DetailView.as_view(),
            name='detail'),
]
