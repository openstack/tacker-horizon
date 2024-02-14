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


class DeletePmThreshold(policy.PolicyTargetMixin, tables.DeleteAction):
    @staticmethod
    def action_present(count):
        return ngettext_lazy(
            "Delete PM Threshold",
            "Delete PM Thresholds",
            count
        )

    @staticmethod
    def action_past(count):
        return ngettext_lazy(
            "Delete PM Threshold",
            "Delete PM Thresholds",
            count
        )

    def action(self, request, obj_id):
        api.tacker.delete_pm_threshold(request, obj_id)


class CreatePmThreshold(tables.LinkAction):
    name = "createpmthreshold"
    verbose_name = _("Create PM Threshold")
    classes = ("ajax-modal",)
    icon = "plus"
    url = "horizon:nfv:vnfpmthreshold:createpmthreshold"


class UpdatePmThreshold(tables.LinkAction):
    name = "updatepmthreshold"
    verbose_name = _("Update PM Threshold")
    url = "horizon:nfv:vnfpmthreshold:updatepmthreshold"
    classes = ("ajax-modal",)


class VnfPmThresholdTable(tables.DataTable):
    id = tables.Column('id', link="horizon:nfv:vnfpmthreshold:detail",
                       verbose_name=_("ID"))
    object_type = tables.Column('object_type', verbose_name=_("Object Type"))
    links = tables.Column('links', verbose_name=_("Links"))

    class Meta(object):
        name = "pmthreshold"
        verbose_name = _("PM Threshold")
        pagination_param = 'vnfpmthreshold_marker'
        prev_pagination_param = 'prev_vnfpmthreshold_marker'
        table_actions = (CreatePmThreshold, DeletePmThreshold,
                         tables.FilterAction,)
        row_actions = (UpdatePmThreshold, DeletePmThreshold,)
