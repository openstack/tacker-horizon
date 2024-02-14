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

from tacker_horizon.openstack_dashboard import api


class VnfLcmRollback(tables.BatchAction):
    name = "vnflcmrollback"
    verbose_name = _("Rollback VNF Lifecycle Management Operation")

    @staticmethod
    def action_present(count):
        return ngettext_lazy(
            "Rollback VNF Lifecycle Management Operation",
            "Rollback VNF Lifecycle Management Operation",
            count
        )

    @staticmethod
    def action_past(count):
        return ngettext_lazy(
            "Rollback VNF Lifecycle Management Operation",
            "Rollback VNF Lifecycle Management Operation",
            count
        )

    def action(self, request, obj_id):
        api.tacker.rollback_vnf_lcm_op_occ(request, obj_id)


class VnfLcmRetry(tables.BatchAction):
    name = "vnflcmretry"
    verbose_name = _("Retry")

    @staticmethod
    def action_present(count):
        return ngettext_lazy(
            "Retry",
            "Retry",
            count
        )

    @staticmethod
    def action_past(count):
        return ngettext_lazy(
            "Retry",
            "Retry",
            count
        )

    def action(self, request, obj_id):
        api.tacker.retry_vnf_lcm_op_occ(request, obj_id)


class VnfLcmFail(tables.BatchAction):
    name = "vnflcmfail"
    verbose_name = _("Fail")

    @staticmethod
    def action_present(count):
        return ngettext_lazy(
            "Fail",
            "Fail",
            count
        )

    @staticmethod
    def action_past(count):
        return ngettext_lazy(
            "Fail",
            "Fail",
            count
        )

    def action(self, request, obj_id):
        api.tacker.fail_vnf_lcm_op_occ(request, obj_id)


class VnfLcmOpOccTable(tables.DataTable):
    id = tables.Column('id', verbose_name=_("ID"),
                       link="horizon:nfv:vnflcmopocc:detail",)
    operation_state = tables.Column('operation_state',
                                    verbose_name=_("OperationState"))
    vnf_instance_id = tables.Column('vnf_instance_id',
                                    verbose_name=_("VNFInstanceID"))
    operation = tables.Column('operation', verbose_name=_("Operation"))

    class Meta(object):
        name = "vnflcmopocc"
        verbose_name = _("VNF LCM OP OCC")
        pagination_param = 'opocc_marker'
        prev_pagination_param = 'prev_opocc_marker'
        table_actions = (VnfLcmRollback, VnfLcmRetry, VnfLcmFail,
                         tables.FilterAction,)
        row_actions = (VnfLcmRollback, VnfLcmRetry, VnfLcmFail,)
        multi_select = True
