from django.contrib import admin
from django.forms.widgets import SelectMultiple
from django.utils.translation import gettext_lazy as _
from django_filters import filters
from django_filters.filters import MultipleChoiceFilter
from django_filters.filterset import FilterSet

from simpel.simpel_products.filters import get_product_child_choices

from .models import SalesOrder


class SalesOrderFilterSet(FilterSet):
    status = filters.MultipleChoiceFilter(
        choices=SalesOrder.STATUS_CHOICES,
        field_name="status",
        label=_("Status"),
    )

    class Meta:
        model = SalesOrder
        fields = ("status",)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.filters["product_type"] = MultipleChoiceFilter(
            label=_("Product Types"),
            field_name="contenttype_id",
            widget=SelectMultiple(),
            choices=get_product_child_choices(key_name="id"),
            help_text=_("Press CTRL + Click to select the choices."),
        )


class OrderAdminFilterSet(admin.SimpleListFilter):
    """Django Admin Product Filter by Polymorphic Type"""

    title = _("Service Type")
    parameter_name = "contenttype_id"

    def lookups(self, request, model_admin):
        return get_product_child_choices(key_name="id")

    def queryset(self, request, queryset):
        if not self.value():
            return queryset

        return queryset.filter(contenttype_id=self.value())
