from rest_framework import serializers
from shared.models.hr_management.hr_masters import Branch


class BranchSerializer(serializers.ModelSerializer):
    class Meta:
        model = Branch
        fields = [
            'id',
            'branch_name',
            'branch_code',
            'address',
            'city',
            'state',
            'zip_code',
            'country_code_number',
            'phone_number',
            'email',
            'status',
            'created_by',
        ]


class BranchListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Branch
        fields = [
            'id',
            'branch_name',
            'branch_code',
            'address',
            'city',
            'state',
            'zip_code',
            'country_code_number',
            'phone_number',
            'email',
            'status',
            'created_by',
            'created_at',
            'updated_at',
            'deleted_at',
        ]
