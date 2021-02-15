import random, string

from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.template.loader import render_to_string
from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, redirect, render
from django.utils import timezone
from django.views.generic import ListView, DetailView
from django.views.generic.base import View
from django.core.mail import EmailMultiAlternatives

from .forms import ItemForm, CheckoutForm, CouponForm
from .models import Item, ItemImages, OrderItem, WishList, Order, Address, Coupon, Payment

def create_ref_code():
    return ''.join(random.choices(string.digits, k=10))

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
        user = get_user(request, True)
        item = get_object_or_404(Item, slug=kwargs['slug'])

        quantity = request.GET.get('quantity')
        if not quantity:
            quantity = 1

        print(user, quantity)
        order_item, created = OrderItem.objects.get_or_create(
            item=item,
            user=user,
            ordered=False
        )
        if created:
            order_item.quantity = int(quantity)
        order_item.save()
        order_qs = Order.objects.filter(user=user, ordered=False)
        if order_qs.exists():
            order = order_qs[0]
            if order.items.filter(item__slug=item.slug).exists():
                order_item.quantity += int(quantity)
                order_item.save()
                return redirect("view cart")
            else:
                order.items.add(order_item)
                return redirect("view cart")
        else:
            ordered_date = timezone.now()
            order = Order.objects.create(
                user=user, ordered_date=ordered_date)
            order.items.add(order_item)
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
            data.append({'title': item.item.title,
                         'id': item.id,
                         'slug': slug,
                         'item': item.item,
                         'discount_price': item.item.discount_price,
                         'price': item.item.price,
                         'quantity': item.quantity,
                         'total': item.get_total_item_price,
                         'image': image.image,
                         })
        if 0 < grand_total_price < 100:
            context['delivery'] = 5
        context['cart_details'] = cart_details
        context['data'] = data
        context['couponform'] = CouponForm()
        context['grand_total_price'] = grand_total_price
        items = Order.objects.filter(user=user, ordered=False)
        context['items'] = items
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


class CheckOutView(View):
    def get(self, *args, **kwargs):
        try:
            user = get_user(self.request, False)
            order = Order.objects.get(user=user, ordered=False)
            form = CheckoutForm()
            context = {
                'form': form,
                'order': order,
                'user': user,
            }
            cart_details = OrderItem.objects.filter(user=user).filter(ordered=False)
            data = []
            for item in cart_details:
                pk = item.item.id
                image = ItemImages.objects.filter(title=pk).first()
                data.append({'title': item.item.title,
                             'id': item.id,
                             'discount_price': item.item.discount_price,
                             'price': item.item.price,
                             'quantity': item.quantity,
                             'total': item.get_total_item_price,
                             'image': image.image})
            context['delivery'] = 0
            context['cart_details'] = cart_details
            context['data'] = data

            items = Order.objects.filter(user=user, ordered=False)
            context['items'] = items

            shipping_address_qs = Address.objects.filter(
                user=user,
                default=True
            )
            if shipping_address_qs.exists():
                context.update(
                    {'default_shipping_address': shipping_address_qs[0]})

            return render(self.request, "checkout.html", context)
        except ObjectDoesNotExist:
            return redirect("view checkout")

    def post(self, *args, **kwargs):
        form = CheckoutForm(self.request.POST or None)
        try:
            user = get_user(self.request, False)
            order = Order.objects.get(user=user, ordered=False)
            if form.is_valid():

                use_default_shipping = form.cleaned_data.get(
                    'use_default_shipping')
                if use_default_shipping:
                    address_qs = Address.objects.filter(
                        user=user,
                        default=True
                    )
                    if address_qs.exists():
                        shipping_address = address_qs[0]
                        order.shipping_address = shipping_address
                        order.save()
                    else:
                        return redirect('view checkout')
                else:
                    first_name = form.cleaned_data.get('first_name')
                    last_name = form.cleaned_data.get('last_name')
                    town = form.cleaned_data.get('town')
                    street_address = form.cleaned_data.get('street_address')
                    apartment_address = form.cleaned_data.get('apartment_address')
                    country = form.cleaned_data.get('country')
                    zip = form.cleaned_data.get('zip')
                    phone = form.cleaned_data.get('phone')
                    email = form.cleaned_data.get('email')

                    if is_valid_form([first_name, last_name, town, street_address,
                                      country, zip, phone, email]):
                        shipping_address, created = Address.objects.get_or_create(
                            user=user,
                            first_name=first_name,
                            last_name=last_name,
                            town=town,
                            street_address=street_address,
                            apartment_address=apartment_address,
                            country=country,
                            zip=zip,
                            phone=phone,
                            email=email
                        )
                        order.shipping_address = shipping_address
                        order.save()

                        set_default_shipping = form.cleaned_data.get(
                            'set_default_shipping')
                        if set_default_shipping:
                            shipping_address.default = True
                            shipping_address.save()

                payment_option = form.cleaned_data.get('payment_option')
                order.payment = Payment.objects.filter(payment_slug=payment_option)[0]
                order.save()

                if payment_option == 'C':
                    return redirect('view payment', payment_option='cash')
                elif payment_option == 'S':
                    return redirect('view payment', payment_option='stripe')
                elif payment_option == 'B':
                    return redirect('view payment', payment_option='bank')
                else:
                    return redirect('view checkout')
            else:
                return redirect("view checkout")
        except ObjectDoesNotExist:
            return redirect("view checkout")


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


def get_coupon(request, code):
    try:
        coupon = Coupon.objects.get(code=code)
        return coupon
    except ObjectDoesNotExist:
        return redirect("view cart")


class AddCouponView(View):
    def post(self, *args, **kwargs):
        form = CouponForm(self.request.POST or None)
        user = get_user(self.request, False)
        if form.is_valid():
            try:
                code = form.cleaned_data.get('code')
                order = Order.objects.get(
                    user=user, ordered=False)
                order.coupon = get_coupon(self.request, code)
                order.save()
                messages.success(self.request, "Successfully added coupon")
                return redirect("view cart")
            except ObjectDoesNotExist:
                messages.info(self.request, "You do not have an active order")
                return redirect("view cart")


class PaymentView(ListView):
    model = Order
    template_name = 'summary.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = get_user(self.request, False)
        items = Order.objects.filter(user=user, ordered=False)

        context['items'] = items
        context['user'] = user

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


class FinishOrder(View):
    def get(self, *args, **kwargs):
        user = get_user(self.request, False)

        try:
            order = Order.objects.get(user=user, ordered=False)
            order_items = order.items.all()
            order_items.update(ordered=True)
            order.ordered = True
            order.ref_code = create_ref_code()
            order.save()
            new_data = Order.objects.filter(ref_code=order.ref_code)
            list_of_items_html = {'shipping': new_data[0], 'items': order_items}
            email_body = render_to_string('email.html', context=list_of_items_html)
            email = EmailMultiAlternatives(f'Поръчка №:{order.ref_code}', email_body, to=['tiger.nuts.bulgaria@gmail.com', order.shipping_address.email])
            email.attach_alternative(email_body, "text/html")
            email.send()
            return redirect("completed order")
        except:
            return redirect("completed order")


def order_success(request):
    user = get_user(request, False)
    context = {
        'message': 'Поръчката е изпратена успешно.',
        'user': user,
    }
    return render(request, "order_success.html", context)


class UserOrders(LoginRequiredMixin, ListView):
    model = Order
    template_name = 'user-orders.html'

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(**kwargs)
        orders = Order.objects.filter(user=self.request.user, ordered=True)
        context['orders'] = orders
        return context


class UserOrderDetails(LoginRequiredMixin, DetailView):
    model = Order
    template_name = 'user-order-summary.html'
    query_pk_and_slug = True
    slug_field = 'ref_code'
    slug_url_kwarg = 'ref_code'

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(**kwargs)
        ref_code = kwargs['object'].ref_code
        items = Order.objects.filter(ref_code=ref_code)
        context['items'] = items

        return context