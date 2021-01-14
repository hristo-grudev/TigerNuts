from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.views.generic import ListView, DetailView

from .models import Item, ItemImages


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
						 'percent': round((1-item.discount_price/item.price)*100),
						 'slug': item.slug,
						 'description': item.description,
						 'image': image.image})
		context['data'] = data
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

		return context


class ContactsView(ListView):
	model = Item
	template_name = 'contact.html'


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
		return context


class AboutView(ListView):
	model = Item
	template_name = 'about.html'


class BlogView(ListView):
	model = Item
	template_name = 'blog.html'


class WishListView(ListView):
	model = Item
	template_name = 'wishlist.html'


class CartView(ListView):
	model = Item
	template_name = 'cart.html'
