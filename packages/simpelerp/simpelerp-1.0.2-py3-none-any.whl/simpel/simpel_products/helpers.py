from django.core.exceptions import ImproperlyConfigured
from django_hookup import core as hookup

from .models import Product
from .settings import simpel_products_settings as products_settings


def get_product_models():
    # Get default products child models from settings
    child_models = products_settings.DEFAULT_PRODUCTS

    # Get products child models from hooks
    funcs = hookup.get_hooks("REGISTER_PRODUCT_CHILD_MODELS")
    registered_child_models = [func() for func in funcs]

    for child_model in registered_child_models:
        if issubclass(child_model, Product):
            if child_model not in child_models:
                child_models.append(child_model)
            else:
                pass
        else:
            raise ImproperlyConfigured(
                "Hook REGISTER_PRODUCT_MODEL should return Product subclass"
            )

    return child_models
