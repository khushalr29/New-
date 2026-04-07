from django.db import models
from ..core.enums import AssetStatus, AssetCondition, DepreciationMethod

class AssetType(models.Model):
    asset_type_name = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(null=True, blank=True)
    updated_at = models.DateTimeField(null=True, blank=True)
    deleted_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        db_table = 'asset_type'
        unique_together = ('asset_type_name',)

    def __str__(self):
        return f"{self.asset_type_name}"

class Assets(models.Model):
    asset_name = models.CharField(max_length=255)
    asset_type = models.ForeignKey(AssetType, on_delete=models.CASCADE, related_name='assets')
    serial_number = models.CharField(max_length=255, unique=True)
    asset_code = models.CharField(max_length=255, unique=True)
    purchase_date = models.DateField()
    purchase_cost = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(max_length=50, choices=AssetStatus.choices)
    condition = models.CharField(max_length=50, choices=AssetCondition.choices)
    description = models.TextField(blank=True, null=True)
    location = models.CharField(max_length=255, blank=True, null=True)
    supplier = models.CharField(max_length=255, blank=True, null=True)
    warranty_information = models.CharField(max_length=255, blank=True, null=True)
    warranty_expiry_date = models.DateField(null=True, blank=True)
    image = models.TextField(blank=True, null=True)
    document = models.TextField(blank=True, null=True)
    depreciation_method = models.CharField(max_length=50, choices=DepreciationMethod.choices)
    useful_life = models.PositiveIntegerField(help_text="Useful life of the asset in years")
    salvage_value = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    created_at = models.DateTimeField(null=True, blank=True)
    updated_at = models.DateTimeField(null=True, blank=True)
    deleted_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        db_table = 'assets'
        unique_together = ('asset_name', 'asset_type')

    def __str__(self):
        return f"{self.asset_name} ({self.asset_type.asset_type_name})"  