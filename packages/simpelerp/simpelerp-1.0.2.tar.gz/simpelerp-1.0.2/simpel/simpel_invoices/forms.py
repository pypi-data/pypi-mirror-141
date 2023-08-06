from django import forms
from django.contrib.admin.widgets import AdminTextareaWidget

from simpel.simpel_sales.settings import simpel_sales_settings as sales_settings

from .models import Invoice

CustomerModel = sales_settings.CUSTOMER_MODEL


class InvoiceAdminForm(forms.ModelForm):
    customer = forms.ModelChoiceField(
        queryset=CustomerModel.objects.filter(is_active=True),
    )
    note = forms.CharField(
        required=False,
        widget=AdminTextareaWidget(attrs={"cols": 70}),
    )

    class Meta:
        model = Invoice
        fields = [
            "group",
            "issued_date",
            "due_date",
            "customer",
            "reference_type",
            "reference_id",
            "discount",
            "note",
        ]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
