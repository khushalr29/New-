from rest_framework import serializers
from shared.models.hr_management import Trip
from ..serializers.employeeSerializer import EmployeeSerializer

class TripsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Trip
        fields = [
            'id',
            'employee',
            'title',
            'description',
            'start_date',
            'end_date',
            'purpose_of_trip',
            'place_of_visit',
            'actual_cost',
            'advance_amount',
            'expected_outcomes',
            'documents',
            'status'
        ]

class TripsListSerializer(serializers.ModelSerializer):
    employee = EmployeeSerializer(read_only=True)
    class Meta:
        model = Trip
        fields = [
            'id',
            'employee',
            'title',
            'description',
            'start_date',
            'end_date',
            'purpose_of_trip',
            'place_of_visit',
            'actual_cost',
            'advance_amount',
            'expected_outcomes',
            'documents',
            'status',
            'company',
            'created_at',
            'updated_at',
            'deleted_at'
        ]