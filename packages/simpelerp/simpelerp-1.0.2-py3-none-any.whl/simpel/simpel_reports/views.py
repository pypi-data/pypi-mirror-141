from django.http.response import HttpResponse
from formtools.wizard.views import SessionWizardView

from .forms import EXPORT_WIZARD_TEMPLATES

# def pay_by_credit_card(wizard):
#     """Return true if user opts to pay by credit card"""
#     # Get cleaned data from payment step
#     cleaned_data = wizard.get_cleaned_data_for_step("paytype") or {"method": "none"}
#     # Return true if the user selected credit card
#     return cleaned_data["method"] == "cc"


class ExportWizardView(SessionWizardView):
    def get_template_names(self):
        return [EXPORT_WIZARD_TEMPLATES[self.steps.current]]

    def done(self, form_list, form_dict, **kwargs):
        """do export using django import export"""
        print(form_dict)
        return HttpResponse("Okk .. exporting")
