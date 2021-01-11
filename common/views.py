from django.contrib import messages
from django.shortcuts import render, redirect
from django.views.generic import ListView, DetailView
from django.views.generic.base import View

from .forms import NewsModal
from .models import Item, ItemImages


class HomePage(ListView):
	model = Item
	template_name = 'home.html'
	context_object_name = 'itmes'

	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)

		items =Item.objects.all()
		context['items'] = items
		print(items)

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
