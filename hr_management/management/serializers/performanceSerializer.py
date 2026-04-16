from rest_framework import serializers
from shared.models.hr_management import IndicatorCategory,Indicator,GoalType,EmployeeGoal,ReviewCycle,EmployeeReview
from management.serializers.employeeSerializer import EmployeeSerializer
from decimal import Decimal

class IndicatorCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = IndicatorCategory
        fields = [
            'id',
            'category_name',
            'description',
            'status'
        ]    

class IndicatorCategoryListSerializer(serializers.ModelSerializer):
    class Meta:
        model = IndicatorCategory
        fields = [
            'id',
            'category_name',
            'description',
            'status',
            'company',
            'created_at',
            'updated_at',
            'deleted_at'
        ]

class IndicatorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Indicator
        fields = [
            'id',
            'indicator_name',
            'category',
            'description',
            'measurement_unit',
            'target_value',
            'status'
        ]

class IndicatorListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Indicator
        fields = [
            'id',
            'indicator_name',
            'category',
            'description',
            'measurement_unit',
            'target_value',
            'status',
            'company',
            'created_at',
            'updated_at',
            'deleted_at'
        ]

class GoalTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = GoalType
        fields = [
            'id',
            'goal_name',
            'description',
            'status'
        ]

class GoalTypeListSerializer(serializers.ModelSerializer):
    class Meta:
        model = GoalType
        fields = [
            'id',
            'goal_name',
            'description',
            'status',
            'company',
            'created_at',
            'updated_at',
            'deleted_at'
        ]

class EmployeeGoalSerializer(serializers.ModelSerializer):
    class Meta:
        model = EmployeeGoal
        fields = [
            'id',
            'employee',
            'goal_type',
            'goal_title',
            'description',
            'start_date',
            'end_date',
            'target',
            'progress_percentage',
            'status'
        ]

class EmployeeGoalListSerializer(serializers.ModelSerializer):
    employee = EmployeeSerializer(read_only=True)
    goal_type = GoalTypeSerializer(read_only=True)
    class Meta:
        model = EmployeeGoal
        fields = [
            'id',
            'employee',
            'goal_type',
            'goal_title',
            'description',
            'start_date',
            'end_date',
            'target',
            'progress_percentage',
            'status',
            'company',
            'created_at',
            'updated_at',
            'deleted_at'
        ]

class ReviewCycleSerializer(serializers.ModelSerializer):
    class Meta:
        model = ReviewCycle
        fields = [
            'id',
            'cycle_name',
            'frequency',
            'description',
            'start_date',
            'end_date',
            'status'
        ]

class ReviewCycleListSerializer(serializers.ModelSerializer):
    class Meta:
        model = ReviewCycle
        fields = [
            'id',
            'cycle_name',
            'frequency',
            'description',
            'start_date',
            'end_date',
            'status',
            'company',
            'created_at',
            'updated_at',
            'deleted_at'
        ]

class EmployeeReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = EmployeeReview
        fields = [
            'id',
            'employee',
            'reviewer',
            'review_cycle',
            'review_date',
            'feedback',
            'rating',
            'status'
        ]    

class EmployeeReviewListSerializer(serializers.ModelSerializer):
    employee = EmployeeSerializer(read_only=True)
    reviewer = EmployeeSerializer(read_only=True)
    review_cycle = ReviewCycleSerializer(read_only=True)
    rating = serializers.DecimalField(max_digits=2, decimal_places=1, max_value=Decimal('5.0'), allow_null=True, required=False)
    class Meta:
        model = EmployeeReview
        fields = [
            'id',
            'employee',
            'reviewer',
            'review_cycle',
            'review_date',
            'feedback',
            'rating',
            'status',
            'company',
            'created_at',
            'updated_at',
            'deleted_at'
        ]