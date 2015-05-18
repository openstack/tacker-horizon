from django.utils.translation import ugettext_lazy as _

from horizon import tables


class MyFilterAction(tables.FilterAction):
    name = "myfilter"


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
        table_actions = (OnBoardVNFLink, MyFilterAction,)
