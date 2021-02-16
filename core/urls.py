from django.urls import path
from .views import ( 
    product,
    HomeView, 
    ItemDetailView,
    OrderSummaryView,
    add_to_cart,
    remove_from_cart,
    remove_single_item_from_cart,
    CheckoutView,
    confirm_purchase,
)
app_name = 'core'

urlpatterns = [
    path('', HomeView.as_view(), name='home'),
    path('checkout/', CheckoutView.as_view(), name='checkout'),
    path('order-summary/', OrderSummaryView.as_view(), name='order-summary'),
    path('product/<slug:slug>', ItemDetailView.as_view(), name='product'),
    path('add_to_cart/<slug:slug>', add_to_cart, name='add-to-cart'),
    path('remove-single-item-from-cart/<slug:slug>/', remove_single_item_from_cart,
         name='remove-single-item-from-cart'),
    path('remove_from_cart/<slug:slug>', remove_from_cart, name='remove-from-cart'),
    path('confirm_purchase/', confirm_purchase, name='confirm-purchase')
]