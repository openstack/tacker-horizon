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
from tacker_horizon.openstack_dashboard.dashboards.nfv.vnffmsubscription \
    import tables


class VnfFmSubscriptionItem(object):
    def __init__(self, subscription_id, callback_uri):
        self.id = subscription_id
        self.name = subscription_id
        self.callback_uri = callback_uri


class VnfFmSubscriptionTab(tabs.TableTab):
    name = _("VNFFMSubscription Tab")
    slug = "vnffmsubscription_tab"
    table_classes = (tables.VnfFmSubscriptionTable,)
    template_name = "horizon/common/_detail_table.html"
    preload = False

    def has_prev_data(self, table):
        return self._has_prev

    def has_more_data(self, table):
        return self._has_more

    def get_subscription_data(self):
        try:
            self._has_prev = False
            page_size = horizon_utils.functions.get_page_size(self.request)
            marker = self.request.GET.get("vnffmsubscription_marker", None)
            prev_marker = self.request.GET.get(
                "prev_vnffmsubscription_marker", None)
            subscriptions = api.tacker.list_fm_subscriptions(self.request)

            if marker is not None or prev_marker is not None:
                for i, subsc in enumerate(subscriptions):
                    if subsc["id"] == marker and i < len(subscriptions) - 1:
                        subscriptions = subscriptions[i + 1:]
                        self._has_prev = True
                        break
                    if subsc["id"] == prev_marker and i > page_size:
                        subscriptions = subscriptions[i - page_size:]
                        self._has_prev = True
                        break

            if len(subscriptions) > page_size:
                self._has_more = True
            else:
                self._has_more = False

            rows = []
            for i, subsc in enumerate(subscriptions):
                if i >= page_size:
                    break
                item = VnfFmSubscriptionItem(subsc['id'],
                                             subsc['callbackUri'])
                rows.append(item)
            return rows
        except Exception:
            self._has_more = False
            error_message = _('Failed to get FM Subscriptions.')
            exceptions.handle(self.request, error_message)
            return []


class VnfFmSubscriptionTabs(tabs.TabGroup):
    slug = "vnffmsubscription_tabs"
    tabs = (VnfFmSubscriptionTab,)
    sticky = True


class VnfFmSubscriptionDetailTab(tabs.Tab):
    name = _("VNF FM Subscription")
    slug = "vnffmsubscription_detail_tab"
    template_name = "nfv/vnffmsubscription/subscription_detail.html"

    def get_context_data(self, request):
        return {'subscription': self.tab_group.kwargs['subscription']}


class VnfFmSubscriptionDetailTabs(tabs.TabGroup):
    slug = "vnffmsubscription_detail_tabs"
    tabs = (VnfFmSubscriptionDetailTab,)
    sticky = True
