from django.db.models import F
from django.shortcuts import get_object_or_404
from django.urls import reverse
from django.views.generic import ListView, DetailView, DeleteView
from django.views.generic.base import RedirectView

from .forms import ItemForm
from .models import Item, ItemImages, OrderItem


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
        if self.request.user != 'AnonymousUser':
            cart_items = 0
        else:
            cart_items = OrderItem.objects.filter(user=self.request.user).filter(ordered=False).count()
        context['cart_items'] = cart_items
        return context


class ItemDetailsView(DetailView):
    model = Item
    template_name = 'products.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        item = context['item']
        item_id = item.id
        images = ItemImages.objects.filter(title__exact=item_id).values('image')
        context['image'] = images[0]['image']
        cart_items = OrderItem.objects.filter(user=self.request.user).filter(ordered=False).count()
        context['cart_items'] = cart_items
        return context


class ContactsView(ListView):
    model = Item
    template_name = 'contact.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        cart_items = OrderItem.objects.filter(user=self.request.user).filter(ordered=False).count()
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
        cart_items = OrderItem.objects.filter(user=self.request.user).filter(ordered=False).count()
        context['cart_items'] = cart_items

        return context


class AboutView(ListView):
    model = Item
    template_name = 'about.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        cart_items = OrderItem.objects.filter(user=self.request.user).filter(ordered=False).count()
        context['cart_items'] = cart_items
        return context


class AddToCart(RedirectView):
    http_method_names = ['post']
    url = '/shop/'

    def post(self, request, *args, **kwargs):
        item_id = kwargs['slug']
        print(item_id)
        item = Item.objects.filter(id__exact=item_id)
        cart_items = OrderItem.objects.filter(ordered=False).filter(user=self.request.user).filter(item=item[0])
        if cart_items:
            cart_items.update(quantity=F('quantity') + 1)
        else:
            OrderItem(user=request.user, ordered=False, item=item[0], quantity=1).save()
        return super(AddToCart, self).post(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        cart_items = OrderItem.objects.filter(user=self.request.user).filter(ordered=False).count()
        context['cart_items'] = cart_items
        return context


class BuyItNow(RedirectView):
    http_method_names = ['post']
    url = '/cart/'

    def post(self, request, *args, **kwargs):
        item_id = kwargs['slug']
        print(item_id)
        item = Item.objects.filter(id__exact=item_id)
        cart_items = OrderItem.objects.filter(ordered=False).filter(user=self.request.user).filter(item=item[0])
        if cart_items:
            cart_items.update(quantity=F('quantity') + 1)
        else:
            OrderItem(user=request.user, ordered=False, item=item[0], quantity=1).save()
        return super(AddToCart, self).post(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        cart_items = OrderItem.objects.filter(user=self.request.user).filter(ordered=False).count()
        context['cart_items'] = cart_items
        return context


class WishListView(ListView):
    model = Item
    template_name = 'wishlist.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        cart_items = OrderItem.objects.filter(user=self.request.user).filter(ordered=False).count()
        context['cart_items'] = cart_items
        return context


class CartView(ListView):
    model = Item
    template_name = 'cart.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        cart_items = OrderItem.objects.filter(user=self.request.user).filter(ordered=False).count()
        cart_details = OrderItem.objects.filter(user=self.request.user).filter(ordered=False)
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
        if grand_total_price < 100:
            context['delivery'] = 5
            grand_total_price += 5
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


class CheckOutView(ListView):
    model = OrderItem
    template_name = 'checkout.html'
