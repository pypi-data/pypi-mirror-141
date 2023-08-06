from django.test import TestCase

from simpel.simpel_products.tests import factories as products_fcs

from . import factories as fcs


class SalesOrderTestCase(TestCase):
    def test_create_sales_order(self):
        sales_order = fcs.SalesOrderFactory()
        sales_order.save()
        product = products_fcs.ServiceFactory()
        product.save()
        sales_order_item = fcs.SalesOrderItemFactory(
            sales_order=sales_order,
            product=product,
            price=product.price,
            quantity=2,
        )
        sales_order_item.save()
