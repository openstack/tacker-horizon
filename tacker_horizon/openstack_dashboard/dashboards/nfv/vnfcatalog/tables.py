# Copyright 2015 Brocade Communications System, Inc.
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


class MyFilterAction(tables.FilterAction):
    name = "myfilter"


class DeleteVNFD(policy.PolicyTargetMixin, tables.DeleteAction):
    @staticmethod
    def action_present(count):
        return ngettext_lazy(
            "Delete VNF",
            "Delete VNFs",
            count
        )

    @staticmethod
    def action_past(count):
        return ngettext_lazy(
            "Delete VNF",
            "Delete VNFs",
            count
        )

    def action(self, request, obj_id):
        api.tacker.delete_vnfd(request, obj_id)


class OnBoardVNF(tables.LinkAction):
    name = "onboardvnf"
    verbose_name = _("Onboard VNF")
    classes = ("ajax-modal",)
    icon = "plus"
    url = "horizon:nfv:vnfcatalog:onboardvnf"


class VNFCatalogTable(tables.DataTable):
    name = tables.Column('name',
                         link="horizon:nfv:vnfcatalog:detail",
                         verbose_name=_("Name"))
    description = tables.Column('description',
                                verbose_name=_("Description"))
    services = tables.Column('service_types',
                             verbose_name=_("Service Types"))
    id = tables.Column('id',
                       verbose_name=_("Catalog Id"))

    class Meta(object):
        name = "vnfcatalog"
        verbose_name = _("VNFCatalog")
        table_actions = (OnBoardVNF, DeleteVNFD, MyFilterAction,)
