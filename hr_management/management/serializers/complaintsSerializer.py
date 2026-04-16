from rest_framework import serializers
from shared.models.hr_management.complaints import Complaint

class ComplaintsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Complaint
        fields = [
            'id',
            'complainant',
            'against_employee',
            'complaint_type',
            'subject',
            'complaint_date',
            'description',
            'document',
            'status',
            'resolution_details',
            'resolved_by',
            'is_submit_anonymously'
        ]

class ComplaintsListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Complaint
        fields = [
            'id',
            'complainant',
            'against_employee',
            'complaint_type',
            'subject',
            'complaint_date',
            'description',
            'document',
            'status',
            'resolution_details',
            'resolved_by',
            'is_submit_anonymously',
            'company',
            'created_at',
            'updated_at',
            'deleted_at'
        ]