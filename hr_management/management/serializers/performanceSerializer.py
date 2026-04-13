from rest_framework import serializer
from shared.models.hr_management import IndicatorCategory,Indicator,GoalType,EmployeeGoal,ReviewCycle,EmployeeReview

class IndicatorCategorySerializer(serializer.ModelSerializer):
    class Meta:
        model = IndicatorCategory
        fields = [
            'id',
            'category_name',
            'description',
            'status'
        ]    

class IndicatorCategoryListSerializer(serializer.ModelSerializer):
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

class IndicatorSerializer(serializer.ModelSerializer):
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

class IndicatorListSerializer(serializer.ModelSerializer):
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

class GoalTypeSerializer(serializer.ModelSerializer):
    class Meta:
        model = GoalType
        fields = [
            'id',
            'goal_name',
            'description',
            'status'
        ]

class GoalTypeListSerializer(serializer.ModelSerializer):
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

class EmployeeGoalSerializer(serializer.ModelSerializer):
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

class EmployeeGoalListSerializer(serializer.ModelSerializer):
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

class ReviewCycleSerializer(serializer.ModelSerializer):
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

class ReviewCycleListSerializer(serializer.ModelSerializer):
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

class EmployeeReviewListSerializer(serializer.ModelSerializer):
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

class EmployeeReviewListSerializer(serializer.ModelSerializer):
    employee = EmployeeSerializer(read_only=True)
    reviewer = EmployeeSerializer(read_only=True)
    review_cycle = ReviewCycleSerializer(read_only=True)
    rating = serializer.DecimalField(max_value=5, decimal_places=1, null=True, blank=True)
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