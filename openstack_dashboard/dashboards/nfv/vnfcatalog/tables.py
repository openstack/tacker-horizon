from django.utils.translation import ugettext_lazy as _
from django.utils.translation import ungettext_lazy

from horizon import tables

from openstack_dashboard import policy

class MyFilterAction(tables.FilterAction):
    name = "myfilter"

class DeleteVNFLink(policy.PolicyTargetMixin, tables.DeleteAction):
    @staticmethod
    def action_present(count):
        return ungettext_lazy(
            u"Delete VNF",
            u"Delete VNF",
            count
        )

    @staticmethod
    def action_past(count):
        return ungettext_lazy(
            u"Delete VNF",
            u"Delete VNF",
            count
        )

class OnBoardVNFLink(tables.LinkAction):
    name = "onboardvnf"
    verbose_name = _("Onboard VNF")
    classes = ("ajax-modal",)
    icon = "plus"
    url = "horizon:nfv:vnfcatalog:onboardvnf"


class VNFCatalogTable(tables.DataTable):
    name = tables.Column('name', \
                         verbose_name=_("Name"))
    description = tables.Column('description', \
                           verbose_name=_("Description"))
    services = tables.Column('services', \
                         verbose_name=_("Services"))
    id = tables.Column('id', \
                         verbose_name=_("Catalog Id"))

    class Meta:
        name = "vnfcatalog"
        verbose_name = _("VNFCatalog")
        table_actions = (OnBoardVNFLink, DeleteVNFLink, MyFilterAction,)
