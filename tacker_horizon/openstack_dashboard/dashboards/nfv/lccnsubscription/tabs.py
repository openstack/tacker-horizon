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
from tacker_horizon.openstack_dashboard.dashboards.nfv.lccnsubscription \
    import tables


class LccnSubscItem(object):
    def __init__(self, subsc_id, callback_uri):
        self.id = subsc_id
        self.name = subsc_id
        self.callback_uri = callback_uri


class LccnSubscriptionTab(tabs.TableTab):
    name = _("LCCN Subscription tab")
    slug = "lccnsubsc_tab"
    table_classes = (tables.LccnSubscriptionTable,)
    template_name = ("horizon/common/_detail_table.html")
    preload = False

    def has_prev_data(self, table):
        return self._has_prev

    def has_more_data(self, table):
        return self._has_more

    def get_lccnsubsc_data(self):
        try:
            self._has_prev = False
            page_size = horizon_utils.functions.get_page_size(self.request)
            marker = self.request.GET.get(
                "subsc_marker", None)
            prev_marker = self.request.GET.get(
                "prev_subsc_marker", None)
            subscs = api.tacker.list_vnf_lcm_subscriptions(
                self.request)
            if marker is not None or prev_marker is not None:
                for i, subsc in enumerate(subscs):
                    if subsc["id"] == marker and i < len(subscs) - 1:
                        subscs = subscs[i + 1:]
                        self._has_prev = True
                        break
                    if subsc["id"] == prev_marker and i > page_size:
                        subscs = subscs[i - page_size:]
                        self._has_prev = True
                        break

            if len(subscs) > page_size:
                self._has_more = True
            else:
                self._has_more = False

            rows = []
            for i, subsc in enumerate(subscs):
                if i >= page_size:
                    break
                item = LccnSubscItem(
                    subsc_id=subsc.get('id', ''),
                    callback_uri=subsc.get('callbackUri', ''))
                rows.append(item)
            return rows
        except Exception:
            self._has_more = False
            error_message = _('Failed to get LCCN Subscriptions.')
            exceptions.handle(self.request, error_message)

            return []


class LccnSubscriptionTabs(tabs.TabGroup):
    slug = "lccnsubsc_tabs"
    tabs = (LccnSubscriptionTab,)
    sticky = True


class LccnSubscDetailTab(tabs.Tab):
    name = _("LCCN Subscription Detail Tab")
    slug = "lccnsubsc_detail_tab"
    template_name = "nfv/lccnsubscription/lccnsubsc_detail.html"

    def get_context_data(self, request):
        return {'lccnsubscription': self.tab_group.kwargs['lccnsubscription']}


class LccnSubscDetailTabs(tabs.TabGroup):
    slug = "lccnsubsc_detail_tabs"
    tabs = (LccnSubscDetailTab,)
    sticky = True
