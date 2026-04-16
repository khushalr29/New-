from rest_framework import serializers
from shared.models.hr_management import TrainingType,TrainingProgram,TrainingSession,AssignTraining
from ..serializers.employeeSerializer import EmployeeSerializer
from ..serializers.branchSerializer import BranchSerializer
from ..serializers.departmentsSerializer import DepartmentSerializer

class TrainingTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = TrainingType
        fields = [
            'id',
            'name',
            'description',
            'branch',
            'departments',
        ]

class TrainingTypeListSerializer(serializers.ModelSerializer):
    branch = BranchSerializer(read_only=True)
    departments = DepartmentSerializer(many=True, read_only=True)
    class Meta:
        model = TrainingType
        fields = [
            'id',
            'name',
            'description',
            'branch',
            'departments',
        ]

class TrainingProgramSerializer(serializers.ModelSerializer):
    class Meta:
        model = TrainingProgram
        fields = [
            'id',
            'name',
            'training_type',
            'description',
            'duration',
            'cost',
            'capacity',
            'status',
            'materials',
            'prequisties',
            'is_mandatory_training',
            'is_allow_self_enrollment'
        ]

class TrainingProgramListSerializer(serializers.ModelSerializer):
    training_type = TrainingTypeListSerializer(read_only=True)
    class Meta:
        model = TrainingProgram
        fields = [
            'id',
            'name',
            'training_type',
            'description',
            'duration',
            'cost',
            'capacity',
            'status',
            'materials',
            'prequisties',
            'is_mandatory_training',
            'is_allow_self_enrollment',
            'company',
            'created_at',
            'updated_at',
            'deleted_at'
        ]        

class TrainingSessionSerializer(serializers.ModelSerializer):
    class Meta:
        model = TrainingSession
        fields = [
            'id',
            'training_program',
            'session_name',
            'start_date',
            'end_date',
            'session_type',
            'location',
            'meeting_link',
            'status',
            'notes',
            'trainer',
            'is_recurring_session',
            'recurrence_pattern',
            'no_of_occurances'
    ]

class TrainingSessionListSerializer(serializers.ModelSerializer):
    training_program = TrainingProgramListSerializer(read_only=True)
    trainer = EmployeeSerializer(read_only=True)
    class Meta:
        model = TrainingSession
        fields = [
            'id',
            'training_program',
            'session_name',
            'start_date',
            'end_date',
            'session_type',
            'location',
            'meeting_link',
            'status',
            'notes',
            'trainer',
            'is_recurring_session',
            'recurrence_pattern',
            'no_of_occurances',
            'company',
            'created_at',
            'updated_at',
            'deleted_at'
        ]

class AssignTrainingSerializer(serializers.ModelSerializer):
    class Meta:
        model = AssignTraining
        fields = [
            'id',
            'employee',
            'training_program',
            'status',
            'assigned_date',
            'completion_date',
            'certification',
            'score',
            'is_passed',
            'feedback',
            'notes',
        
    ]

class AssignTrainingListSerializer(serializers.ModelSerializer):
    employee = EmployeeSerializer(read_only=True)
    training_program = TrainingProgramListSerializer(read_only=True)
    class Meta:
        model = AssignTraining
        fields = [
            'id',
            'employee',
            'training_program',
            'status',
            'assigned_date',
            'completion_date',
            'certification',
            'score',
            'is_passed',
            'feedback',
            'notes',
            'company',
            'created_at',
            'updated_at',
            'deleted_at'
        ]
    