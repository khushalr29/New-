from rest_framework import serializers
from ..enums import (DependencyPermissions,UploadCategory,SubscriptionModels,BillingModels,
                     CoreModels,PrintAppModelS)
from shared.models.core.enums import (Gender, )

class EnumSerializer(serializers.Serializer):
    name = serializers.CharField()
    value = serializers.CharField()

class UploadCategorySerializers(EnumSerializer):
    class Meta:
        model = UploadCategory
        fields = ['name', 'value']

class SubscriptionModelSerializer(EnumSerializer):
    class Meta:
        model = SubscriptionModels
        fields = ['name', 'value']

class BillingModelSerializer(EnumSerializer):
    class Meta:
        model = BillingModels
        fields = ['name', 'value']

class CoreModelSerializer(EnumSerializer):
    class Meta:
        model = CoreModels
        fields = ['name', 'value']

class PrintModelSerializer(EnumSerializer):
    class Meta:
        model = PrintAppModelS
        fields = ['name', 'value']

class DependencyPermissionsSerializer(EnumSerializer):
    class Meta:
        model = DependencyPermissions
