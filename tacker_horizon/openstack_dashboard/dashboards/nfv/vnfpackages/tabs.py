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


from django.utils.translation import gettext_lazy as _

from horizon import exceptions
from horizon import tabs
from horizon import utils as horizon_utils

from tacker_horizon.openstack_dashboard import api
from tacker_horizon.openstack_dashboard.dashboards.nfv import utils  # noqa
from tacker_horizon.openstack_dashboard.dashboards.nfv.vnfpackages \
    import tables


class VnfPackageItem(object):
    def __init__(self, vnfpkg_id, vnf_product_name, onboarding_state,
                 usage_state, operational_state, vnfd_id,):
        self.id = vnfpkg_id
        self.name = vnfpkg_id
        self.vnf_product_name = vnf_product_name
        self.onboarding_state = onboarding_state
        self.usage_state = usage_state
        self.operational_state = operational_state
        self.vnfd_id = vnfd_id


class VnfPackageTab(tabs.TableTab):
    name = _("VNFP tab")
    slug = "vnfpkg_tab"
    table_classes = (tables.VnfPackageTable,)
    template_name = ("horizon/common/_detail_table.html")
    preload = False

    def has_prev_data(self, table):
        return self._has_prev

    def has_more_data(self, table):
        return self._has_more

    def get_vnfpackage_data(self):
        try:
            self._has_prev = False
            page_size = horizon_utils.functions.get_page_size(self.request)
            marker = self.request.GET.get(
                "package_marker", None)
            prev_marker = self.request.GET.get(
                "prev_package_marker", None)
            packages = api.tacker.list_vnf_packages(self.request)
            if marker is not None or prev_marker is not None:
                for i, package in enumerate(packages):
                    if package["id"] == marker and i < len(packages) - 1:
                        packages = packages[i + 1:]
                        self._has_prev = True
                        break
                    if package["id"] == prev_marker and i > page_size:
                        packages = packages[i - page_size:]
                        self._has_prev = True
                        break

            if len(packages) > page_size:
                self._has_more = True
            else:
                self._has_more = False

            rows = []
            for i, package in enumerate(packages):
                if i >= page_size:
                    break
                item = VnfPackageItem(
                    vnfpkg_id=package.get('id', ''),
                    vnf_product_name=package.get('vnfProductName', ''),
                    onboarding_state=package.get('onboardingState', ''),
                    usage_state=package.get('usageState', ''),
                    operational_state=package.get('operationalState', ''),
                    vnfd_id=package.get('vnfdId', ''),)
                rows.append(item)
            return rows
        except Exception:
            self._has_more = False
            error_message = _('Failed to get VNF Packages.')
            exceptions.handle(self.request, error_message)

            return []


class VnfPackageTabs(tabs.TabGroup):
    slug = "vnfpkg_tabs"
    tabs = (VnfPackageTab,)
    sticky = True


class VnfPackageDetailTab(tabs.Tab):
    name = _("VNFPkg Detail")
    slug = "vnfpkg_detail_tab"
    template_name = "nfv/vnfpackages/vnfpkg_detail.html"

    def get_context_data(self, request):
        return {'vnfpkg': self.tab_group.kwargs['vnfpkg']}


class VnfPackageDetailTabs(tabs.TabGroup):
    slug = "vnfpkg_detail_tabs"
    tabs = (VnfPackageDetailTab,)
    sticky = True
