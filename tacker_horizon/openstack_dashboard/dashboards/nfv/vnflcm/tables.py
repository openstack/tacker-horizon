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


class DeleteVnfIdentifier(policy.PolicyTargetMixin, tables.DeleteAction):
    @staticmethod
    def action_present(count):
        return ngettext_lazy(
            "Delete VNF Identifier",
            "Delete VNF Identifiers",
            count
        )

    @staticmethod
    def action_past(count):
        return ngettext_lazy(
            "Delete VNF Identifier",
            "Delete VNF Identifiers",
            count
        )

    def action(self, request, obj_id):
        api.tacker.delete_vnf_instance(request, obj_id)


class CreateVnfIdentifier(tables.LinkAction):
    name = "createvnfid"
    verbose_name = _("Create VNF Identifier")
    url = "horizon:nfv:vnflcm:createvnfidentifier"
    classes = ("ajax-modal",)
    icon = "plus"


class InstantiateVnf(tables.LinkAction):
    name = "instantiatevnf"
    verbose_name = _("Instantiate VNF")
    url = "horizon:nfv:vnflcm:instantiatevnf"
    classes = ("ajax-modal",)


class TerminateVnf(tables.LinkAction):
    name = "terminate_vnf"
    verbose_name = _("Terminate VNF")
    url = "horizon:nfv:vnflcm:terminatevnf"
    classes = ("ajax-modal",)


class HealVnf(tables.LinkAction):
    name = "heal_vnf"
    verbose_name = _("Heal VNF")
    url = "horizon:nfv:vnflcm:healvnf"
    classes = ("ajax-modal",)


class UpdateVnf(tables.LinkAction):
    name = "update_Vnf"
    verbose_name = _("Update VNF")
    url = "horizon:nfv:vnflcm:updatevnf"
    classes = ("ajax-modal",)


class ScaleVnf(tables.LinkAction):
    name = "scale_vnf"
    verbose_name = _("Scale VNF")
    url = "horizon:nfv:vnflcm:scalevnf"
    classes = ("ajax-modal",)


class ChangeExternalVnfConnectivity(tables.LinkAction):
    name = "change_external_vnf_connectivity"
    verbose_name = _("Change External VNF Connectivity")
    url = "horizon:nfv:vnflcm:changeconnectivity"
    classes = ("ajax-modal",)


class ChangeCurrentVnfPackage(tables.LinkAction):
    name = "change_current_vnf_package"
    verbose_name = _("Change Current VNF Package")
    url = "horizon:nfv:vnflcm:changevnfpkg"
    classes = ("ajax-modal",)


class VnfLcmTable(tables.DataTable):
    id = tables.Column('id', verbose_name=_("ID"),
                       link="horizon:nfv:vnflcm:detail",)
    vnf_instance_name = tables.Column('vnf_instance_name',
                                      verbose_name=_("VNF Instance Name"))
    instantiation_state = tables.Column('instantiation_state',
                                        verbose_name=_("Instantiation State"))
    vnf_provider = tables.Column('vnf_provider',
                                 verbose_name=_("VNF Provider"))
    vnf_software_version = tables.Column(
        'vnf_software_version',
        verbose_name=_("VNF Software Version"))
    vnf_product_name = tables.Column('vnf_product_name',
                                     verbose_name=_("VNF Product Name"))
    vnfd_id = tables.Column('vnfd_id', verbose_name=_("VNFD ID"))

    class Meta(object):
        name = "vnflcm"
        verbose_name = _("VNF LCM")
        pagination_param = 'vnflcm_marker'
        prev_pagination_param = 'prev_vnflcm_marker'
        table_actions = (CreateVnfIdentifier, DeleteVnfIdentifier,
                         tables.FilterAction,)
        row_actions = (InstantiateVnf, TerminateVnf, DeleteVnfIdentifier,
                       HealVnf, UpdateVnf, ScaleVnf,
                       ChangeExternalVnfConnectivity, ChangeCurrentVnfPackage,)
