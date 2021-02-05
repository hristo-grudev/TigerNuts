from django.urls import path

from common.views import HomePage, ItemDetailsView, ContactsView, ShopView, AboutView, AddToCart, WishListView, \
	CartView, RemoveItemFromCart, CheckOutView, AddToFavorites, MakeOrder, AddCouponView, OrderSummaryView

urlpatterns = [
	path('', HomePage.as_view(), name='view home'),
	path('contacts/', ContactsView.as_view(), name='view contacts'),
	path('shop/', ShopView.as_view(), name='view shop'),
	path('shop/<slug:slug>', ItemDetailsView.as_view(), name='view item'),
	path('about/', AboutView.as_view(), name='view about'),
	path('wishlist/', WishListView.as_view(), name='view wishlist'),
	path('cart/', CartView.as_view(), name='view cart'),
	path('add-to-cart/<slug:slug>/', AddToCart.as_view(), name='add-to-cart'),
	path('remove-from-cart/<slug:slug>/', RemoveItemFromCart.as_view(), name='remove-from-cart'),
	path('checkout/', CheckOutView.as_view(), name='view checkout'),
	path('add-to-favorites/<slug:slug>/', AddToFavorites.as_view(), name='add-to-favorites'),
	path('order/', MakeOrder.as_view(), name='make order'),
	path('coupon/', AddCouponView.as_view(), name='add coupon'),
	path('summary/', OrderSummaryView.as_view(), name='view summary'),
]
