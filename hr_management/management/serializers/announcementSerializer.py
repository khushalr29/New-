from rest_framework import serializers
from shared.models.hr_management.announcement import Announcement
from .departmentsSerializer import DepartmentSerializer
from .branchSerializer import BranchSerializer

class AnnouncementSerializer(serializers.ModelSerializer):
    class Meta:
        model = Announcement
        fields = [
            'id',
            'title',
            'category',
            'short_description',
            'content',
            'start_date',
            'end_date',
            'attachment',
            'is_featured_announcement',
            'is_high_priority',
            'is_company_wide_announcement',
            'branch',
            'department'
        ]

class AnnouncementListSerializer(serializers.ModelSerializer):
    branch = BranchSerializer(read_only=True)
    department  = DepartmentSerializer(read_only=True)
    class Meta:
        model = Announcement
        fields = [
            'id',
            'title',
            'category',
            'short_description',
            'content',
            'start_date',
            'end_date',
            'attachment',
            'is_featured_announcement',
            'is_high_priority',
            'is_company_wide_announcement',
            'branch',
            'department',
            'created_at',
            'updated_at',
            'deleted_at'
        ]    