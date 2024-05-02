from django.urls import path
from django.views.generic import RedirectView
from .views import VendorListCreate, VendorRetrieveUpdateDestroy, PurchaseOrderListCreate, PurchaseOrderRetrieveUpdateDestroy,AcknowledgePurchaseOrder

urlpatterns = [
    path('', RedirectView.as_view(url='/vendors/')),
    path('vendors/', VendorListCreate.as_view(), name='vendor-list-create'),
    path('vendors/<int:pk>/', VendorRetrieveUpdateDestroy.as_view(), name='vendor-retrieve-update-destroy'),
    path('vendors/<int:pk>/', VendorRetrieveUpdateDestroy.as_view(), name='vendor-retrieve-update-destroy'),
    path('purchase_orders/', PurchaseOrderListCreate.as_view(), name='purchase-order-list-create'),
    path('purchase_orders/<int:pk>/', PurchaseOrderRetrieveUpdateDestroy.as_view(), name='purchase-order-retrieve-update-destroy'),
    path('purchase_orders/<int:pk>/acknowledge/', AcknowledgePurchaseOrder.as_view(), name='acknowledge-purchase-order'),
]
