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
from django.utils.translation import ngettext_lazy

from horizon import tables
from openstack_dashboard import policy

from tacker_horizon.openstack_dashboard import api


class DeleteLccnSubscription(policy.PolicyTargetMixin, tables.DeleteAction):
    @staticmethod
    def action_present(count):
        return ngettext_lazy(
            "Delete Lccn Subscription",
            "Delete Lccn Subscriptions",
            count
        )

    @staticmethod
    def action_past(count):
        return ngettext_lazy(
            "Delete Lccn Subscription",
            "Delete Lccn Subscriptions",
            count
        )

    def action(self, request, obj_id):
        api.tacker.delete_vnf_lcm_subscription(request, obj_id)


class CreateLccnSubscription(tables.LinkAction):
    name = "create_lccnsubsc"
    verbose_name = _("Create Lccn Subscription")
    classes = ("ajax-modal",)
    icon = "plus"
    url = "horizon:nfv:lccnsubscription:createlccnsubscription"


class LccnSubscriptionTable(tables.DataTable):
    id = tables.Column('id', verbose_name=_("ID"),
                       link="horizon:nfv:lccnsubscription:detail",)
    callback_uri = tables.Column('callback_uri',
                                 verbose_name=_("Callback URI"))

    class Meta(object):
        name = "lccnsubsc"
        verbose_name = _("LCCN Subscription")
        pagination_param = 'subsc_marker'
        prev_pagination_param = 'prev_subsc_marker'
        table_actions = (CreateLccnSubscription, DeleteLccnSubscription,
                         tables.FilterAction)
        row_actions = (DeleteLccnSubscription,)
        multi_select = True
