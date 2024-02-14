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


class DeleteVnfFmSubscription(policy.PolicyTargetMixin, tables.DeleteAction):
    @staticmethod
    def action_present(count):
        return ngettext_lazy(
            "Delete Subscription",
            "Delete Subscriptions",
            count
        )

    @staticmethod
    def action_past(count):
        return ngettext_lazy(
            "Delete Subscription",
            "Delete Subscriptions",
            count
        )

    def action(self, request, obj_id):
        api.tacker.delete_fm_subscription(request, obj_id)


class CreateVnfFmSubscription(tables.LinkAction):
    name = "createsubscription"
    verbose_name = _("Create Subscription")
    classes = ("ajax-modal",)
    icon = "plus"
    url = "horizon:nfv:vnffmsubscription:createsubscription"


class VnfFmSubscriptionTable(tables.DataTable):
    id = tables.Column('id', link="horizon:nfv:vnffmsubscription:detail",
                       verbose_name=_("ID"))
    callback_uri = tables.Column('callback_uri',
                                 verbose_name=_("Callback Uri"))

    class Meta(object):
        name = "subscription"
        verbose_name = _("Subscription")
        pagination_param = 'vnffmsubscription_marker'
        prev_pagination_param = 'prev_vnffmsubscription_marker'
        table_actions = (CreateVnfFmSubscription, DeleteVnfFmSubscription,
                         tables.FilterAction,)
        row_actions = (DeleteVnfFmSubscription,)
