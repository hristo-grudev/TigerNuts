from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from django.db.models import F
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404
from django.urls import reverse, reverse_lazy
from django.views.generic import ListView, DetailView, DeleteView, CreateView, FormView
from django.views.generic.base import RedirectView

from .forms import ItemForm, CheckoutForm
from .models import Item, ItemImages, OrderItem, WishList, Order, Address


def get_cart_items(request, create):
    try:
        device = request.COOKIES['device']
    except:
        device = ''
    devices = User.objects.filter(username__exact=device).exists()
    if request.user.is_authenticated:
        user = request.user.id
    else:
        if not devices and create is True:
            user, created = User.objects.get_or_create(username=device)
        else:
            user = User.objects.filter(username__exact=device).first()

    cart_items = OrderItem.objects.filter(user=user).filter(ordered=False).count()
    return cart_items


class HomePage(ListView):
    model = Item
    template_name = 'home.html'
    context_object_name = 'itmes'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        items = Item.objects.all()
        data = []
        for item in items:
            pk = item.id
            image = ItemImages.objects.filter(title=pk).first()
            data.append({'id': item.id,
                         'title': item.title,
                         'discount_price': item.discount_price,
                         'price': item.price,
                         'percent': round((1 - item.discount_price / item.price) * 100),
                         'slug': item.slug,
                         'description': item.description,
                         'image': image.image})
        context['data'] = data
        cart_items = get_cart_items(self.request, False)
        context['cart_items'] = cart_items

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
        device = self.request.COOKIES['device']

        devices = User.objects.filter(username__exact=device).exists()

        if self.request.user.is_authenticated:
            user = self.request.user
        else:
            if not devices:
                user, created = User.objects.get_or_create(username=device)
            else:
                user = User.objects.filter(username__exact=device).first()

        cart_items = OrderItem.objects.filter(user=user).filter(ordered=False).count()
        context['cart_items'] = cart_items
        return context


class ContactsView(ListView):
    model = Item
    template_name = 'contact.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        cart_items = get_cart_items(self.request, False)
        context['cart_items'] = cart_items
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
                         'discount_price': item.discount_price,
                         'price': item.price,
                         'percent': round((1 - item.discount_price / item.price) * 100),
                         'slug': item.slug,
                         'description': item.description,
                         'image': image.image})
        context['data'] = data
        cart_items = get_cart_items(self.request, False)
        context['cart_items'] = cart_items

        return context


class AboutView(ListView):
    model = Item
    template_name = 'about.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        cart_items = get_cart_items(self.request, False)
        context['cart_items'] = cart_items
        return context


class AddToCart(RedirectView):
    http_method_names = ['post']
    url = '/shop/'

    def post(self, request, *args, **kwargs):
        item_id = kwargs['slug']

        device = self.request.COOKIES['device']

        devices = User.objects.filter(username__exact=device).exists()

        if self.request.user.is_authenticated:
            user = self.request.user
        else:
            if not devices:
                user, created = User.objects.get_or_create(username=device)
            else:
                user = User.objects.filter(username__exact=device).first()

        item = Item.objects.filter(id__exact=item_id)
        print(item, user)
        cart_items = OrderItem.objects.filter(ordered=False).filter(user=user).filter(item=item[0])
        quantity = request.POST.get('quantity')
        if quantity is None:
            quantity = 1
        if cart_items:
            cart_items.update(quantity=F('quantity') + quantity)
        else:
            OrderItem(user=user, ordered=False, item=item[0], quantity=quantity).save()
        return super(AddToCart, self).post(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        cart_items = get_cart_items(self.request, True)
        context['cart_items'] = cart_items
        return context

    def get_redirect_url(self, *args, **kwargs):
        _id = self.kwargs['slug']
        item = Item.objects.filter(id__exact=_id).first()
        return reverse_lazy('view item', kwargs={'slug': str(item.slug)})


class BuyItNow(RedirectView):
    http_method_names = ['post']
    url = '/cart/'

    def post(self, request, *args, **kwargs):
        item_id = kwargs['slug']

        device = self.request.COOKIES['device']

        devices = User.objects.filter(username__exact=device).exists()

        if self.request.user.is_authenticated:
            user = self.request.user
        else:
            if not devices:
                user, created = User.objects.get_or_create(username=device)
            else:
                user = User.objects.filter(username__exact=device).first()

        item = Item.objects.filter(id__exact=item_id)
        print(item, user)
        cart_items = OrderItem.objects.filter(ordered=False).filter(user=user).filter(item=item[0])
        quantity = request.POST.get('quantity')
        if quantity is None:
            quantity = 1
        if cart_items:
            cart_items.update(quantity=F('quantity') + quantity)
        else:
            OrderItem(user=user, ordered=False, item=item[0], quantity=quantity).save()
        return super(BuyItNow, self).post(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        cart_items = get_cart_items(self.request, True)
        context['cart_items'] = cart_items
        return context


class WishListView(ListView):
    model = Item
    template_name = 'wishlist.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        try:
            device = self.request.COOKIES['device']
        except:
            device = ''
        if self.request.user.is_authenticated:
            user = self.request.user.id
        else:
            user = User.objects.filter(username__exact=device).first()
        wish_list = WishList.objects.filter(user=user)
        context['wish_list'] = wish_list
        data = []
        for item in wish_list:
            pk = item.item
            image = ItemImages.objects.filter(title=pk).first()
            item_details = Item.objects.filter(title=pk)
            data.append({'id': item_details[0].id,
                         'title': item_details[0].title,
                         'discount_price': item_details[0].discount_price,
                         'price': item_details[0].price,
                         'percent': round((1 - item_details[0].discount_price / item_details[0].price) * 100),
                         'slug': item_details[0].slug,
                         'description': item_details[0].description,
                         'image': image.image})

        cart_items = get_cart_items(self.request, False)
        context['cart_items'] = cart_items
        context['data'] = data
        return context


class CartView(ListView):
    model = Item
    template_name = 'cart.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        cart_items = get_cart_items(self.request, False)
        if self.request.user.is_authenticated:
            user = self.request.user
        else:
            device = self.request.COOKIES['device']
            user = User.objects.filter(username__exact=device).first()
        cart_details = OrderItem.objects.filter(user=user).filter(ordered=False)
        context['cart_items'] = cart_items
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


class RemoveItemFromCart(DeleteView):

    def get_object(self):
        obj_id = self.kwargs.get('id')
        return get_object_or_404(OrderItem, id=obj_id)

    def get_success_url(self):
        return reverse('view cart')


class CheckOutView(CreateView):
    model = Address
    template_name = 'checkout.html'
    # fields = '__all__'
    form_class = CheckoutForm

    def get_success_url(self):
        slug = self.kwargs['slug']
        return reverse_lazy('make order', kwargs={'slug': str(slug)})

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        cart_items = get_cart_items(self.request, False)
        if self.request.user.is_authenticated:
            user = self.request.user
        else:
            device = self.request.COOKIES['device']
            user = User.objects.filter(username__exact=device).first()
        cart_details = OrderItem.objects.filter(user=user).filter(ordered=False)
        context['cart_items'] = cart_items
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


class AddToFavorites(RedirectView):
    model = WishList
    # success_url = '/shop/'
    http_method_names = ['post']
    url = '/shop/'

    def post(self, request, *args, **kwargs):
        item_id = kwargs['id']
        device = self.request.COOKIES['device']

        devices = User.objects.filter(username__exact=device).exists()

        if self.request.user.is_authenticated:
            user = self.request.user
        else:
            if not devices:
                user, created = User.objects.get_or_create(username=device)
            else:
                user = User.objects.filter(username__exact=device).first()

        item = Item.objects.filter(id__exact=item_id)
        try:
            WishList.objects.get(user=user, item=item[0]).delete()
        except:
            WishList(user=user, item=item[0]).save()

        return super(AddToFavorites, self).post(request, *args, **kwargs)


class MakeOrder(ListView):
    model = WishList
    template_name = 'order_complete.html'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)

        return context

    def post(self, *args, **kwargs):
        pass