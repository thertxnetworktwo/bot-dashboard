from django.db import models
from datetime import datetime, timedelta
import uuid


class ProductStatus(models.TextChoices):
    ACTIVE = 'Active', 'Active'
    EXPIRED = 'Expired', 'Expired'
    EXPIRING_SOON = 'ExpiringSoon', 'Expiring Soon'


class Product(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False, db_index=True)
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    bot_username = models.CharField(max_length=255, blank=True, null=True)
    website_link = models.CharField(max_length=500, blank=True, null=True)
    contract_months = models.IntegerField()  # 1-12 months
    contract_start_date = models.DateTimeField()
    contract_end_date = models.DateTimeField()
    is_renewed = models.BooleanField(default=False)
    status = models.CharField(
        max_length=20,
        choices=ProductStatus.choices,
        default=ProductStatus.ACTIVE,
        db_index=True
    )
    customer_telegram = models.CharField(max_length=255, blank=True, null=True, db_index=True)
    customer_link = models.CharField(max_length=500, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'products'
        ordering = ['-created_at']

    def save(self, *args, **kwargs):
        # Calculate contract_end_date if not set
        if self.contract_start_date and self.contract_months and not self.contract_end_date:
            self.contract_end_date = self.contract_start_date + timedelta(days=30 * self.contract_months)
        
        # Update status before saving
        self.update_status()
        super().save(*args, **kwargs)

    def update_status(self):
        """Update product status based on contract dates."""
        if not self.contract_end_date:
            return
        
        now = datetime.now(self.contract_end_date.tzinfo) if self.contract_end_date.tzinfo else datetime.utcnow()
        days_until_expiry = (self.contract_end_date - now).days
        
        if days_until_expiry < 0:
            self.status = ProductStatus.EXPIRED
        elif days_until_expiry <= 7:
            self.status = ProductStatus.EXPIRING_SOON
        else:
            self.status = ProductStatus.ACTIVE

    def __str__(self):
        return self.name
