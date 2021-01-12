from django.urls import path

from common.views import HomePage, ItemDetailsView, ContactsView, ShopView, AboutView, BlogView, WishListView, CartView

urlpatterns = [
	path('', HomePage.as_view(), name='view home'),
	path('contacts/', ContactsView.as_view(), name='view contacts'),
	path('shop/', ShopView.as_view(), name='view shop'),
	path('shop/<int:pk>', ItemDetailsView.as_view(), name='view item'),
	path('about/', AboutView.as_view(), name='view about'),
	path('wishlist/', WishListView.as_view(), name='view wishlist'),
	path('cart/', CartView.as_view(), name='view cart'),
]
