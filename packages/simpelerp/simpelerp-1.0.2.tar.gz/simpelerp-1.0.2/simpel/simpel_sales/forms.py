from django import forms

from .models import SalesOrder, SalesQuotation
from .settings import simpel_sales_settings as sales_settings

CustomerModel = sales_settings.CUSTOMER_MODEL


class SalesOrderForm(forms.ModelForm):
    customer = forms.ModelChoiceField(
        queryset=CustomerModel.objects.filter(is_active=True),
    )

    class Meta:
        model = SalesOrder
        fields = [
            "group",
            "customer",
            "reference",
            "discount",
            "note",
            "status",
        ]


class SalesQuotationForm(forms.ModelForm):
    customer = forms.ModelChoiceField(
        queryset=CustomerModel.objects.filter(is_active=True),
    )

    class Meta:
        model = SalesQuotation
        fields = [
            "group",
            "customer",
            "note",
        ]
