from django.shortcuts import render

# Create your views here.
from rest_framework import generics ,status
from .models import Vendor, PurchaseOrder
from .serializers import VendorSerializer, PurchaseOrderSerializer
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import PurchaseOrder

class VendorListCreate(generics.ListCreateAPIView):
    queryset = Vendor.objects.all()
    serializer_class = VendorSerializer

class VendorRetrieveUpdateDestroy(generics.RetrieveUpdateDestroyAPIView):
    queryset = Vendor.objects.all()
    serializer_class = VendorSerializer

    def get_performance_metrics(self, vendor):
        performance_metrics = {
            "on_time_delivery_rate": vendor.on_time_delivery_rate,
            "quality_rating_avg": vendor.quality_rating_avg,
            "average_response_time": vendor.average_response_time,
            "fulfillment_rate": vendor.fulfillment_rate,
        }
        return performance_metrics

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        performance_metrics = self.get_performance_metrics(instance)
        response_data = serializer.data
        response_data['performance_metrics'] = performance_metrics
        return Response(response_data)

# class VendorRetrieveUpdateDestroy(generics.RetrieveUpdateDestroyAPIView):
#     queryset = Vendor.objects.all()
#     serializer_class = VendorSerializer

class PurchaseOrderListCreate(generics.ListCreateAPIView):
    queryset = PurchaseOrder.objects.all()
    serializer_class = PurchaseOrderSerializer

class PurchaseOrderRetrieveUpdateDestroy(generics.RetrieveUpdateDestroyAPIView):
    queryset = PurchaseOrder.objects.all()
    serializer_class = PurchaseOrderSerializer


class AcknowledgePurchaseOrder(APIView):
    def post(self, request, pk):
        try:
            purchase_order = PurchaseOrder.objects.get(pk=pk)
        except PurchaseOrder.DoesNotExist:
            return Response({"error": "Purchase order does not exist"}, status=status.HTTP_404_NOT_FOUND)

        # Perform acknowledgment logic here, e.g., update acknowledgment_date
        
        # Trigger recalculation of average response time
        purchase_order.vendor.calculate_performance_metrics()

        return Response({"message": "Purchase order acknowledged successfully"}, status=status.HTTP_200_OK)

