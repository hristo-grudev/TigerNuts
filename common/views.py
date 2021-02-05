from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist
from django.db.models import F
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse, reverse_lazy
from django.utils import timezone
from django.views.generic import ListView, DetailView, DeleteView, CreateView, FormView, UpdateView
from django.views.generic.base import RedirectView, View

from .forms import ItemForm, CheckoutForm, CouponForm
from .models import Item, ItemImages, OrderItem, WishList, Order, Address, Coupon


def is_valid_form(values):
    valid = True
    for field in values:
        if field == '':
            valid = False
    return valid


def get_user(request, create):
    try:
        device = request.COOKIES['device']
    except:
        device = ''
    devices = User.objects.filter(username__exact=device).exists()
    if request.user.is_authenticated:
        user = request.user
    else:
        if not devices and create is True:
            user, created = User.objects.get_or_create(username=device)
        else:
            user = User.objects.filter(username__exact=device).first()

    return user


class HomePage(ListView):
    model = Item
    template_name = 'home.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        items = Item.objects.all()
        data = []
        for item in items:
            pk = item.id
            image = ItemImages.objects.filter(title=pk).first()
            data.append({'id': item.id,
                         'title': item.title,
                         'item': item,
                         'discount_price': item.discount_price,
                         'price': item.price,
                         'percent': round((1 - item.discount_price / item.price) * 100),
                         'slug': item.slug,
                         'description': item.description,
                         'image': image.image})
        context['data'] = data
        print(data)
        user = get_user(self.request, False)
        context['user'] = user

        return context


class ItemDetailsView(DetailView):
    model = Item
    template_name = 'products.html'
    query_pk_and_slug = True

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        print(self.request.POST)
        item = context['item']
        item_id = item.id
        images = ItemImages.objects.filter(title__exact=item_id).values('image')
        context['image'] = images[0]['image']
        context['form'] = ItemForm  # marker

        user = get_user(self.request, False)
        context['user'] = user
        return context


class ContactsView(ListView):
    model = Item
    template_name = 'contact.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = get_user(self.request, False)
        context['user'] = user
        return context


class ShopView(ListView):
    model = Item
    template_name = 'shop.html'

    # paginate_by = 1

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        items = Item.objects.all()
        data = []
        for item in items:
            pk = item.id
            image = ItemImages.objects.filter(title=pk).first()
            data.append({'id': item.id,
                         'title': item.title,
                         'item': item,
                         'discount_price': item.discount_price,
                         'price': item.price,
                         'percent': round((1 - item.discount_price / item.price) * 100),
                         'slug': item.slug,
                         'description': item.description,
                         'image': image.image})
        context['data'] = data
        user = get_user(self.request, False)
        context['user'] = user

        return context


class AboutView(ListView):
    model = Item
    template_name = 'about.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = get_user(self.request, False)
        context['user'] = user
        return context


class AddToCart(View):

    def get(self, request, *args, **kwargs):
        item = get_object_or_404(Item, slug=kwargs['slug'])
        quantity = request.POST.get('quantity')
        if not quantity:
            quantity = 1
        user = get_user(request, True)
        print(user, quantity)
        order_item, created = OrderItem.objects.get_or_create(
            item=item,
            user=user,
            ordered=False,
            quantity=quantity
        )
        order_qs = Order.objects.filter(user=user, ordered=False)
        if order_qs.exists():
            order = order_qs[0]
            if order.items.filter(item__slug=item.slug).exists():
                order_item.quantity += quantity
                order_item.save()
                return redirect("view cart")
            else:
                order.items.add(order_item)
                messages.info(request, "This item was added to your cart.")
                return redirect("view cart")
        else:
            ordered_date = timezone.now()
            order = Order.objects.create(
                user=user, ordered_date=ordered_date)
            order.items.add(order_item)
            messages.info(request, "This item was added to your cart.")
            return redirect("view cart")


class BuyItNow(View):

    def get(self, request, *args, **kwargs):
        item = get_object_or_404(Item, slug=kwargs['slug'])
        quantity = request.POST.get('quantity')
        if not quantity:
            quantity = 1
        user = get_user(request, True)
        print(user, quantity)
        order_item, created = OrderItem.objects.get_or_create(
            item=item,
            user=user,
            ordered=False,
            quantity=quantity
        )
        order_qs = Order.objects.filter(user=user, ordered=False)
        if order_qs.exists():
            order = order_qs[0]
            if order.items.filter(item__slug=item.slug).exists():
                order_item.quantity += quantity
                order_item.save()
                return redirect("view cart")
            else:
                order.items.add(order_item)
                messages.info(request, "This item was added to your cart.")
                return redirect("view cart")
        else:
            ordered_date = timezone.now()
            order = Order.objects.create(
                user=user, ordered_date=ordered_date)
            order.items.add(order_item)
            messages.info(request, "This item was added to your cart.")
            return redirect("view cart")


class WishListView(ListView):
    model = Item
    template_name = 'wishlist.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = get_user(self.request, False)
        context['user'] = user
        wish_list = WishList.objects.filter(user=user)
        context['wish_list'] = wish_list
        data = []
        for item in wish_list:
            pk = item.item
            image = ItemImages.objects.filter(title=pk).first()
            item_details = Item.objects.filter(title=pk)
            data.append({'id': item_details[0].id,
                         'title': item_details[0].title,
                         'item': item.item,
                         'discount_price': item_details[0].discount_price,
                         'price': item_details[0].price,
                         'percent': round((1 - item_details[0].discount_price / item_details[0].price) * 100),
                         'slug': item_details[0].slug,
                         'description': item_details[0].description,
                         'image': image.image})

        context['data'] = data
        return context


class CartView(ListView):
    model = Item
    template_name = 'cart.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = get_user(self.request, False)
        context['user'] = user
        cart_details = OrderItem.objects.filter(user=user, ordered=False)
        data = []
        grand_total_price = 0
        for item in cart_details:
            pk = item.item.id
            slug = item.item.slug
            image = ItemImages.objects.filter(title=pk).first()
            grand_total_price += item.get_total_item_price()
            data.append({'title': item.item.title,
                         'id': item.id,
                         'slug': slug,
                         'item': item.item,
                         'discount_price': item.item.discount_price,
                         'price': item.item.price,
                         'quantity': item.quantity,
                         'total': item.get_total_item_price,
                         'image': image.image})
        context['delivery'] = 0
        if 0 < grand_total_price < 100:
            context['delivery'] = 5
        context['cart_details'] = cart_details
        context['data'] = data
        context['grand_total_price'] = grand_total_price
        return context


class RemoveItemFromCart(View):

    def get(self, request, **kwargs):
        item = get_object_or_404(Item, slug=kwargs['slug'])
        user = get_user(request, False)
        order_qs = Order.objects.filter(
            user=user,
            ordered=False
        )
        if order_qs.exists():
            order = order_qs[0]
            if order.items.filter(item__slug=item.slug).exists():
                order_item = OrderItem.objects.filter(
                    item=item,
                    user=user,
                    ordered=False
                )[0]
                order.items.remove(order_item)
                order_item.delete()
                return redirect("view cart")
            else:
                return redirect("view item", slug=kwargs['slug'])
        else:
            return redirect("view item", slug=kwargs['slug'])


class CheckOutView(FormView):
    model = Address
    template_name = 'checkout.html'
    # fields = '__all__'
    form_class = CheckoutForm

    def get_success_url(self):
        slug = self.kwargs['slug']
        return reverse_lazy('make order', kwargs={'slug': str(slug)})

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        user = get_user(self.request, False)
        context['user'] = user
        cart_details = OrderItem.objects.filter(user=user).filter(ordered=False)
        data = []
        grand_total_price = 0
        for item in cart_details:
            pk = item.item.id
            image = ItemImages.objects.filter(title=pk).first()
            grand_total_price += item.get_total_item_price()
            data.append({'title': item.item.title,
                         'id': item.id,
                         'discount_price': item.item.discount_price,
                         'price': item.item.price,
                         'quantity': item.quantity,
                         'total': item.get_total_item_price,
                         'image': image.image})
        context['delivery'] = 0
        if 0 < grand_total_price < 100:
            context['delivery'] = 5
        context['cart_details'] = cart_details
        context['data'] = data
        context['grand_total_price'] = grand_total_price
        return context


class AddToFavorites(View):

    def get(self, request, *args, **kwargs):
        item_slug = kwargs['slug']
        user = get_user(request, True)

        item = Item.objects.filter(slug__exact=item_slug)
        try:
            WishList.objects.get(user=user, item=item[0]).delete()
        except:
            WishList(user=user, item=item[0]).save()

        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


class MakeOrder(View):
    def get(self, *args, **kwargs):
        try:
            order = Order.objects.get(user=self.request.user, ordered=False)
            form = CheckoutForm()
            context = {
                'form': form,
                'couponform': CouponForm(),
                'order': order,
                'DISPLAY_COUPON_FORM': True
            }

            shipping_address_qs = Address.objects.filter(
                user=self.request.user,
                address_type='S',
                default=True
            )
            if shipping_address_qs.exists():
                context.update(
                    {'default_shipping_address': shipping_address_qs[0]})

            billing_address_qs = Address.objects.filter(
                user=self.request.user,
                address_type='B',
                default=True
            )
            if billing_address_qs.exists():
                context.update(
                    {'default_billing_address': billing_address_qs[0]})
            return render(self.request, "checkout.html", context)
        except ObjectDoesNotExist:
            messages.info(self.request, "You do not have an active order")
            return redirect("core:checkout")

    def post(self, *args, **kwargs):
        form = CheckoutForm(self.request.POST or None)
        try:
            order = Order.objects.get(user=self.request.user, ordered=False)
            if form.is_valid():

                use_default_shipping = form.cleaned_data.get(
                    'use_default_shipping')
                if use_default_shipping:
                    print("Using the defualt shipping address")
                    address_qs = Address.objects.filter(
                        user=self.request.user,
                        default=True
                    )
                    if address_qs.exists():
                        shipping_address = address_qs[0]
                        order.shipping_address = shipping_address
                        order.save()
                    else:
                        messages.info(
                            self.request, "No default shipping address available")
                        return redirect('view checkout')
                else:
                    print("User is entering a new shipping address")
                    shipping_address1 = form.cleaned_data.get(
                        'street_address')
                    shipping_address2 = form.cleaned_data.get(
                        'apartment_address')
                    shipping_country = form.cleaned_data.get(
                        'country')
                    shipping_zip = form.cleaned_data.get('shipping_zip')

                    if is_valid_form([shipping_address1, shipping_country, shipping_zip]):
                        shipping_address = Address(
                            user=self.request.user,
                            street_address=shipping_address1,
                            apartment_address=shipping_address2,
                            country=shipping_country,
                            zip=shipping_zip
                        )
                        shipping_address.save()

                        order.shipping_address = shipping_address
                        order.save()

                        set_default_shipping = form.cleaned_data.get(
                            'set_default_shipping')
                        if set_default_shipping:
                            shipping_address.default = True
                            shipping_address.save()

                    else:
                        messages.info(
                            self.request, "Please fill in the required shipping address fields")

                payment_option = form.cleaned_data.get('payment_option')

                if payment_option == 'C':
                    return redirect('core:payment', payment_option='card')
                elif payment_option == 'P':
                    return redirect('core:payment', payment_option='paypal')
                else:
                    messages.warning(
                        self.request, "Invalid payment option selected")
                    return redirect('view checkout')
        except ObjectDoesNotExist:
            messages.warning(self.request, "You do not have an active order")
            return redirect("view summary")


def get_coupon(request, code):
    try:
        coupon = Coupon.objects.get(code=code)
        return coupon
    except ObjectDoesNotExist:
        messages.info(request, "This coupon does not exist")
        return redirect("view cart")


class AddCouponView(View):
    def post(self, *args, **kwargs):
        form = CouponForm(self.request.POST or None)
        if form.is_valid():
            try:
                code = form.cleaned_data.get('code')
                order = Order.objects.get(
                    user=self.request.user, ordered=False)
                order.coupon = get_coupon(self.request, code)
                order.save()
                messages.success(self.request, "Successfully added coupon")
                return redirect("view cart")
            except ObjectDoesNotExist:
                messages.info(self.request, "You do not have an active order")
                return redirect("view cart")


class OrderSummaryView(LoginRequiredMixin, ListView):
    model = Order
    template_name = 'summary.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        items = Order.objects.filter(user=self.request.user)
        print(items)
        context['items'] = items

        return context


def remove_single_item_from_cart(request, slug):
    item = get_object_or_404(Item, slug=slug)
    user = get_user(request, False)
    order_qs = Order.objects.filter(
        user=user,
        ordered=False
    )
    if order_qs.exists():
        order = order_qs[0]
        # check if the order item is in the order
        if order.items.filter(item__slug=item.slug).exists():
            order_item = OrderItem.objects.filter(
                item=item,
                user=user,
                ordered=False
            )[0]
            if order_item.quantity > 1:
                order_item.quantity -= 1
                order_item.save()
            else:
                order.items.remove(order_item)
            messages.info(request, "This item quantity was updated.")
            return redirect("view cart")
        else:
            messages.info(request, "This item was not in your cart")
            return redirect("view item", slug=slug)
    else:
        messages.info(request, "You do not have an active order")
        return redirect("view item", slug=slug)