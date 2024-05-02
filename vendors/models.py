from django.db import models

# Create your models here.
from django.db.models import Avg, Count
from django.utils import timezone

# Create your models here.

class Vendor(models.Model):
    name = models.CharField(max_length=100)
    contact_details = models.TextField()
    address = models.TextField()
    vendor_code = models.CharField(max_length=20, unique=True)
    on_time_delivery_rate = models.FloatField(default=0)
    quality_rating_avg = models.FloatField(default=0)
    average_response_time = models.FloatField(default=0)
    fulfillment_rate = models.FloatField(default=0)

    def __str__(self):
        return self.name
    def calculate_performance_metrics(self):
        # Calculate on-time delivery rate
        completed_orders = self.purchaseorder_set.filter(status='completed')
        total_completed_orders = completed_orders.count()
        if total_completed_orders > 0:
            on_time_orders = completed_orders.filter(delivery_date__lte=timezone.now())
            on_time_delivery_rate = (on_time_orders.count() / total_completed_orders) * 100
            self.on_time_delivery_rate = round(on_time_delivery_rate, 2)
        else:
            self.on_time_delivery_rate = 0
        
        # Calculate quality rating average
        self.quality_rating_avg = self.purchaseorder_set.filter(quality_rating__isnull=False).aggregate(Avg('quality_rating'))['quality_rating__avg'] or 0
        
        # Calculate average response time
        acknowledgment_times = self.purchaseorder_set.filter(acknowledgment_date__isnull=False).annotate(response_time=models.F('acknowledgment_date') - models.F('issue_date')).aggregate(Avg('response_time'))['response_time__avg']
        self.average_response_time = acknowledgment_times.total_seconds() if acknowledgment_times else 0
        
        # Calculate fulfillment rate
        total_orders = self.purchaseorder_set.count()
        if total_orders > 0:
            successful_orders = self.purchaseorder_set.filter(status='completed')
            fulfillment_rate = (successful_orders.count() / total_orders) * 100
            self.fulfillment_rate = round(fulfillment_rate, 2)
        else:
            self.fulfillment_rate = 0

        # Save the changes
        self.save()

class PurchaseOrder(models.Model):
    po_number = models.CharField(max_length=50, unique=True)
    vendor = models.ForeignKey(Vendor, on_delete=models.CASCADE)
    order_date = models.DateTimeField()
    delivery_date = models.DateTimeField(null=True, blank=True)
    items = models.JSONField()
    quantity = models.IntegerField()
    status = models.CharField(max_length=20)
    quality_rating = models.FloatField(null=True, blank=True)
    issue_date = models.DateTimeField()
    acknowledgment_date = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return self.po_number
    
    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        # Update vendor performance metrics after saving purchase order
        self.vendor.calculate_performance_metrics()

    def delete(self, *args, **kwargs):
        vendor = self.vendor
        super().delete(*args, **kwargs)
        # Update vendor performance metrics after deleting purchase order
        vendor.calculate_performance_metrics()

class HistoricalPerformance(models.Model):
    vendor = models.ForeignKey(Vendor, on_delete=models.CASCADE)
    date = models.DateTimeField()
    on_time_delivery_rate = models.FloatField()
    quality_rating_avg = models.FloatField()
    average_response_time = models.FloatField()
    fulfillment_rate = models.FloatField()

    def __str__(self):
        return f"{self.vendor.name} - {self.date}"

