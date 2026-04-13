from rest_framework import serializer
from shared.models.hr_management.complaints import Complaint

class ComplaintSerializer(serializer.ModelSerializer):
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

class ComplaintListSerializer(serializer.ModelSerializer):
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
            'company',
            'created_at',
            'updated_at',
            'deleted_at'
        ]