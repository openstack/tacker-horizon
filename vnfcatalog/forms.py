from django.core.urlresolvers import reverse
from django.utils.translation import ugettext_lazy as _

from horizon import exceptions
from horizon import forms

from openstack_dashboard import api

class OnBoardVNF(forms.SelfHandlingForm):
    name = forms.CharField(max_length=80, label=_("VNF Name"), required=False)
    image_id = forms.ChoiceField(
        label=_("Image Name"),
        required=False,
        widget=forms.SelectWidget(
            data_attrs=('volume_size',)))
    binding = forms.CharField(
        required=False,
        max_length=80, label=_("Network Binding"))

    def handle(self, request, data):
        try:
	    fields = {}
            return api.heat.stack_create(self.request, **fields)
        except Exception:
            exceptions.handle(request,
                              _('Unable to create service.'))

