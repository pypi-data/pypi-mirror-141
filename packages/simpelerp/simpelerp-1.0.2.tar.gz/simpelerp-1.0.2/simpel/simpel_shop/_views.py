from django.contrib import messages
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse
from django.utils.translation import gettext_lazy as _
from simpel_admin.base import AdminFormView, AdminTemplateView

from simpel.simpel_shop import models as cart_models
from simpel.simpel_shop.forms import CartItemBundleForm, CheckoutForm


class AdminCartView(AdminTemplateView):
    title = _("Shopping Cart")
    template_name = "admin/simpel_shop/cart.html"

    def get_cart(self):
        cart = cart_models.Cart.get_for_user(self.request.user)
        return cart

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update(
            {
                "cart": self.get_cart(),
                "title": self.title,
                "detail_action": True,
            }
        )
        return context

    def post(self, request, *args, **kwargs):
        cid = request.POST.get("id")
        act = request.POST.get("action")
        if not cid:
            messages.error(request, _("Invalid form value."))
            return redirect(reverse("simpeladmin:mycart"))
        self.item = get_object_or_404(cart_models.CartItem, pk=cid)
        if not self.item.cart.user == request.user:
            messages.error(request, _("You dont have permission to update this item"))

        # Update Quantity
        if act == "update_item":
            self.item.quantity = int(request.POST.get("quantity", 1))
            self.item.save()
            messages.success(request, _("Item %s updated") % self.item)

        # Create copy of Cart Item as Blueprint
        if act == "save_as_blueprint":
            try:
                cart_models.BluePrint.clone(request.user, self.item)
                messages.success(request, _("Cart item %s blueprint created.") % self.item)
                return redirect(reverse("simpeladmin:myblueprints"))
            except Exception as err:
                print(err)
                messages.error(request, _("Cart item %s blueprint creation failed.") % self.item)

        # Remove Cart Item Confirmation
        if act == "remove_item":
            return self.render_confirm(request, *args, **kwargs)

        # Remove Item Confirmed
        if act == "remove_item_confirm":
            self.item.delete()
            messages.success(request, _("Remove cart item %s") % self.item)
        return redirect(reverse("simpeladmin:mycart"))

    def render_confirm(self, request, *args, **kwargs):
        self.title = _("Deleting %s") % self.item
        context = self.get_context_data(**kwargs)
        context.update({"removed_item": self.item})
        return self.render_to_response(context)


class AdminCartAddItemParameterView(AdminFormView):
    template_name = "simpel_admin/form_view.html"

    def dispatch(self, request, pk, *args, **kwargs):
        self.cart_item = get_object_or_404(cart_models.CartItem, pk=pk)
        if self.cart_item.cart.user != request.user:
            messages.error(request, _("You dont have permission to update this item"))
            return redirect(reverse("simpeladmin:mycart"))
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = _("Adding Parameter to `%s`") % self.cart_item
        context["cancel_url"] = reverse("simpeladmin:mycart")
        return context

    def get_form_class(self):
        return CartItemBundleForm

    def get_initial(self):
        return {"cart_item": self.cart_item}

    def get_success_url(self):
        messages.success(self.request, _("%s added to %s") % (self.instance, self.cart_item))
        return reverse("simpeladmin:mycart")

    def form_valid(self, form):
        self.instance = form.save(commit=False)
        self.instance.cart_item = self.cart_item
        self.instance.save()
        return super().form_valid(form)


class AdminCartRemoveItemParameterView(AdminTemplateView):
    template_name = "simpel_admin/confirm_delete.html"

    def dispatch(self, request, pk, *args, **kwargs):
        self.object = get_object_or_404(cart_models.CartItemBundle, pk=pk)
        if self.object.cart_item.cart.user != request.user:
            messages.error(request, _("You dont have permission to delete this item"))
            return redirect(reverse("simpeladmin:mycart"))
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["opts"] = self.object.product._meta
        context["title"] = _("Delete Parameter %s from `%s`") % (self.object, self.object.cart_item)
        context["cancel_url"] = reverse("simpeladmin:mycart")
        return context

    def get_success_url(self):
        messages.success(self.request, _("%s added to %s") % (self.instance, self.cart_item))
        return reverse("simpeladmin:mycart")

    def post(self, request, *args, **kwargs):
        self.object.delete()
        messages.success(request, _("%s removed from %s.") % (self.object, self.object.cart_item))
        return redirect(reverse("simpeladmin:mycart"))


class AdminCartCheckoutView(AdminFormView):
    template_name = "simpel_admin/form_view.html"
    form_class = CheckoutForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = _("Create Order")
        context["cancel_url"] = reverse("simpeladmin:mycart")
        return context

    def get_success_url(self):
        messages.success(self.request, _("Order created, complete payment and send confirmation."))
        return reverse("simpeladmin:mycart")

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs.update({"request": self.request})
        return kwargs

    def form_valid(self, form):
        form.save()
        return redirect(reverse("simpeladmin:mycart"))


class AdminMyBlueprintsView(AdminTemplateView):
    title = _("Blueprints")
    template_name = "simpel_admin/simpel_shop/blueprints.html"

    def get_blueprints(self):
        blueprints = self.request.user.blueprints.all()
        return blueprints

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({"title": self.title, "blueprints": self.get_blueprints()})
        return context

    def post(self, request, *args, **kwargs):
        bid = request.POST.get("id")
        act = request.POST.get("action")
        if not bid:
            messages.error(request, _("Invalid form value."))
            return redirect(reverse("simpeladmin:myblueprints"))
        self.item = get_object_or_404(cart_models.BluePrint, pk=bid)
        if not self.item.user == request.user:
            messages.error(request, _("You dont have permission to update this item."))
        if act == "remove_blueprint":
            return self.render_confirm(request, *args, **kwargs)
        if act == "add_to_cart":
            try:
                cart_models.BluePrint.add_to_cart(self.item, request.POST["quantity"])
                messages.success(request, _("Succesfully add %s blueprint.") % self.item)
                return redirect(reverse("simpeladmin:mycart"))
            except Exception as err:
                print(err)
                messages.error(request, _("Failed to add %s blueprint to cart.") % self.item)
        if act == "remove_blueprint_confirm":
            self.item.delete()
            messages.success(request, _("Remove %s blueprint.") % self.item)
        return redirect(reverse("simpeladmin:myblueprints"))

    def render_confirm(self, request, *args, **kwargs):
        self.title = _("Deleting %s") % self.item
        context = self.get_context_data(**kwargs)
        context.update({"removed_item": self.item})
        return self.render_to_response(context)
