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

from horizon import exceptions
from horizon import messages
from horizon import tables
from openstack_dashboard import policy

from tacker_horizon.openstack_dashboard import api


class DeleteVnfPackage(policy.PolicyTargetMixin, tables.DeleteAction):
    @staticmethod
    def action_present(count):
        return ngettext_lazy(
            "Delete VNF Package",
            "Delete VNF Packages",
            count
        )

    @staticmethod
    def action_past(count):
        return ngettext_lazy(
            "Delete VNF Package",
            "Delete VNF Packages",
            count
        )

    def action(self, request, obj_id):
        api.tacker.delete_vnf_package(request, obj_id)


class UploadVnfPackage(tables.LinkAction):
    name = "uploadvnfpkg"
    verbose_name = _("Upload VNF Package")
    classes = ("ajax-modal",)
    icon = "plus"
    url = "horizon:nfv:vnfpackages:uploadvnfpkg"


class FetchVnfPackage(tables.LinkAction):
    name = "fetchvnfpkg"
    verbose_name = _("Fetch VNF Package")
    verbose_name_plural = _("Fetch VNF Package")
    icon = "download"
    url = "horizon:nfv:vnfpackages:fetch"

    def allowed(self, request, datum=None):
        return True


class UpdateVnfPackageInfo(tables.LinkAction):
    name = "updatevnfpkginfo"
    verbose_name = _("Update VNF Package Info")
    url = "horizon:nfv:vnfpackages:updatevnfpkg"
    classes = ("ajax-modal",)


class CreateVnfIdentifier(tables.Action):
    name = "createvnfid"
    verbose_name = _("Create VNF Identifier")

    def single(self, table, request, obj_id):  # pylint: disable=E0202
        try:
            vnf_pkg = api.tacker.get_vnf_package(request, obj_id)
            vnfd_id = vnf_pkg.get('vnfdId', None)
            if not vnfd_id:
                msg = _('Failed to get VNFD ID')
                raise Exception(msg)
            req_body = {}
            req_body['vnfdId'] = vnfd_id
            response = api.tacker.create_vnf_instance(request, req_body)
            messages.success(request,
                             _('Create VNF Identifier. (id: %s)') %
                             response['id'])
        except Exception:
            exceptions.handle(request,
                              _('Failed to create VNF Identifier.'))


class VnfPackageTable(tables.DataTable):
    id = tables.Column('id', verbose_name=_("ID"),
                       link="horizon:nfv:vnfpackages:detail",)
    name = tables.Column('vnf_product_name',
                         verbose_name=_("VNF Product Name"))
    onboarding_state = tables.Column('onboarding_state',
                                     verbose_name=_("Onboarding State"))
    usage_state = tables.Column('usage_state', verbose_name=_("Usage State"))
    operational_state = tables.Column('operational_state',
                                      verbose_name=_("Operational State"))

    class Meta(object):
        name = "vnfpackage"
        verbose_name = _("VNF Package")
        pagination_param = 'package_marker'
        prev_pagination_param = 'prev_package_marker'
        table_actions = (UploadVnfPackage, DeleteVnfPackage,
                         tables.FilterAction,)
        row_actions = (FetchVnfPackage, UpdateVnfPackageInfo, DeleteVnfPackage,
                       CreateVnfIdentifier,)
