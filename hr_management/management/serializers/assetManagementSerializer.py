from rest_framework import serializer
from shared.models.hr_management.asset_manage import AssetType, Assets

class AssetTypeSerializer(serializer.ModelSerializer):
    class Meta:
        model = AssetType
        fields = [
            'id',
            'asset_type_name',
            'description'
        ]

class AssetSerializer(serializer.ModelSerializer):
    class Meta:
        model = Assets
        fields = [
            'id',
            'asset_name',
            'asset_type',
            'serial_number',
            'asset_code',
            'purchase_date',
            'purchase_cost',
            'status',
            'condition',
            'description',
            'location',
            'supplier',
            'warranty_information',
            'warranty_expiry_date',
            'image',
            'document',
            'depreciation_method',
            'useful_life',
            'salvage_value'
        ]

class AssetListSerializer(serializer.ModelSerializer):
    asset_type = AssetTypeSerializer(read_only=True)

    class Meta:
        model = Assets
        fields = [
            'id',
            'asset_name',
            'asset_type',
            'serial_number',
            'asset_code',
            'purchase_date',
            'purchase_cost',
            'status',
            'condition',
            'description',
            'location',
            'supplier',
            'warranty_information',
            'warranty_expiry_date',
            'image',
            'document',
            'depreciation_method',
            'useful_life',
            'salvage_value',
            'created_at',
            'updated_at',
            'deleted_at'
        ]