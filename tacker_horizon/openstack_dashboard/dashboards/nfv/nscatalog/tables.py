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


class DeleteNSD(policy.PolicyTargetMixin, tables.DeleteAction):
    @staticmethod
    def action_present(count):
        return ngettext_lazy(
            "Delete NS",
            "Delete NSs",
            count
        )

    @staticmethod
    def action_past(count):
        return ngettext_lazy(
            "Delete NS",
            "Delete NSs",
            count
        )

    def action(self, request, obj_id):
        api.tacker.delete_nsd(request, obj_id)


class OnBoardNS(tables.LinkAction):
    name = "onboardns"
    verbose_name = _("Onboard NS")
    classes = ("ajax-modal",)
    icon = "plus"
    url = "horizon:nfv:nscatalog:onboardns"


class NSCatalogTable(tables.DataTable):
    name = tables.Column('name',
                         link="horizon:nfv:nscatalog:detail",
                         verbose_name=_("Name"))
    description = tables.Column('description',
                                verbose_name=_("Description"))
    id = tables.Column('id',
                       verbose_name=_("Catalog Id"))

    class Meta(object):
        name = "nscatalog"
        verbose_name = _("NSCatalog")
        table_actions = (OnBoardNS, DeleteNSD, MyFilterAction,)
