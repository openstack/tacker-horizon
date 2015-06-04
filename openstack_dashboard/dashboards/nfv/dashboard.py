from django.utils.translation import ugettext_lazy as _

import horizon

class Nfvgroup(horizon.PanelGroup):
    slug = "nfvgroup"
    name = _("VNF Management")
    panels = ('vnfcatalog', 'vnfmanager',)


class Nfv(horizon.Dashboard):
    name = _("NFV")
    slug = "nfv"
    panels = (Nfvgroup,)  # Add your panels here.
    default_panel = 'vnfcatalog'  # Specify the slug of the dashboard's default panel.


horizon.register(Nfv)
