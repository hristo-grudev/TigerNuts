from django.urls import path

from common.views import HomePage, ItemDetailsView, ContactsView, ShopView, AboutView, AddToCart, WishListView, \
	CartView, RemoveItemFromCart, CheckOutView, BuyItNow, AddToFavorites, AddCouponView, PaymentView, FinishOrder, \
	order_success, UserOrders, UserOrderDetails

urlpatterns = [
	path('', HomePage.as_view(), name='view home'),
	path('contacts/', ContactsView.as_view(), name='view contacts'),
	path('shop/', ShopView.as_view(), name='view shop'),
	path('shop/<slug:slug>', ItemDetailsView.as_view(), name='view item'),
	path('about/', AboutView.as_view(), name='view about'),
	path('wishlist/', WishListView.as_view(), name='view wishlist'),
	path('cart/', CartView.as_view(), name='view cart'),
	path('add-to-cart/<slug:slug>/', AddToCart.as_view(), name='add-to-cart'),
	# path('add-to-cart/<slug:slug>/', AddToCart.as_view(), name='add-to-cart'),
	path('remove-from-cart/<slug:slug>/', RemoveItemFromCart.as_view(), name='remove-from-cart'),
	# path('remove-from-cart/<slug:slug>/', RemoveItemFromCart.as_view(), name='remove-from-cart'),
	path('checkout/', CheckOutView.as_view(), name='view checkout'),
	path('buy-it-now/<slug:slug>/', BuyItNow.as_view(), name='buy-it-now'),
	path('add-to-favorites/<slug:slug>/', AddToFavorites.as_view(), name='add-to-favorites'),
	path('coupon/', AddCouponView.as_view(), name='add coupon'),
	# path('summary/', OrderSummaryView.as_view(), name='view summary'),
	path('payment/<payment_option>/', PaymentView.as_view(), name='view payment'),
	path('finish/', FinishOrder.as_view(), name='finish order'),
	path('order-completed/', order_success, name='completed order'),
	path('my-orders/', UserOrders.as_view(), name='view orders'),
	path('my-orders/<ref_code>/', UserOrderDetails.as_view(), name='view order'),
]
