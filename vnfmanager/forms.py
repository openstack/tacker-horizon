from django.core.urlresolvers import reverse
from django.utils.translation import ugettext_lazy as _

from horizon import exceptions
from horizon import forms

from openstack_dashboard import api


class AddService(forms.SelfHandlingForm):
    VNF = forms.ChoiceField(
        label=_("VNF"),
        choices=[('vyatta', _('Vyatta vRouter')),
                 ('f5', _('F5 Networks')),
                 ('palo', _('Palo Alto')),
                 ('cisco', _('CISCO'))],)
    flavor = forms.ChoiceField(
        label=_("Flavor"),
        choices=[('lht', _('Large High Throughout')),
                 ('mhm', _('Medium High Memory'))],)
    groups = forms.MultipleChoiceField(label=_("Services"),
                                       required=False,
                                       choices=(('nat','NAT'), ('fw','firewall'), ('vpn','VPN')),
                                       widget=forms.CheckboxSelectMultiple(),
                                       help_text=_("Launch instance in these "
                                                   "security groups."))

    def handle(self, request, data):
        try:
	    fields = {}
            return api.heat.stack_create(self.request, **fields)
        except Exception:
            exceptions.handle(request,
                              _('Unable to create service.'))
