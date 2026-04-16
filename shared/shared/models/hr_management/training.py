from django.db import models
from .hr_masters import Branch
from ..core.enums import TrainingStatus, MeetingType, RecurrenceType, SessionStatus, AssignTrainingStatus
from ..core.base import TenantModel

class TrainingType(TenantModel):
    name = models.CharField(max_length=255)
    description = models.TextField(null=True, blank=True)
    branch = models.ForeignKey(Branch, on_delete=models.CASCADE, related_name='training_types')
    departments = models.ManyToManyField('shared.Department', related_name='training_types', blank=True)

    class Meta:
        db_table = 'training_type'

    def __str__(self):
        return self.name

class TrainingProgram(TenantModel):
    name = models.CharField(max_length=255)
    training_type = models.ForeignKey(TrainingType, on_delete=models.CASCADE, related_name='programs')
    description = models.TextField(null=True, blank=True)
    duration = models.PositiveIntegerField(default=0)
    cost = models.DecimalField(max_digits=15, decimal_places=2, default=0.00)
    capacity = models.PositiveIntegerField(default=0)
    status = models.CharField(max_length=20, choices=TrainingStatus.choices, default=TrainingStatus.ACTIVE)
    materials = models.TextField(null=True, blank=True)
    prequisties = models.TextField(null=True, blank=True)
    is_mandatory_training = models.BooleanField(default=True)
    is_allow_self_enrollment = models.BooleanField(default=True)

    class Meta:
        db_table = 'training_program'

    def __str__(self):
        return self.name

class TrainingSession(TenantModel):
    training_program = models.ForeignKey(TrainingProgram, on_delete=models.CASCADE, related_name='sessions')
    session_name = models.CharField(max_length=255, null=True, blank=True)
    start_date = models.DateField()
    end_date = models.DateField()
    session_type = models.CharField(max_length=20, choices=MeetingType.choices)
    location = models.CharField(max_length=255, null=True, blank=True)
    meeting_link = models.CharField(max_length=255, null=True, blank=True)
    status = models.CharField(max_length=20, choices=SessionStatus.choices, default=SessionStatus.SCHEDULED)
    notes = models.TextField(null=True, blank=True)
    trainer = models.ForeignKey('shared.Employee', on_delete=models.SET_NULL, null=True, blank=True, related_name='training_sessions')
    is_recurring_session = models.BooleanField(default=False)
    recurrence_pattern = models.CharField(max_length=20, choices=RecurrenceType.choices, null=True, blank=True)
    no_of_occurances = models.PositiveIntegerField(default=0)

    class Meta:
        db_table = 'training_session'

    def __str__(self):
        return self.session_name or f"Session for {self.training_program.name}"

class AssignTraining(TenantModel):
    employee = models.ForeignKey('shared.Employee', on_delete=models.CASCADE, related_name='assigned_trainings')
    training_program = models.ForeignKey(TrainingProgram, on_delete=models.CASCADE, related_name='assigned_employees')
    status = models.CharField(max_length=50, choices=AssignTrainingStatus.choices, default=AssignTrainingStatus.PENDING)
    assigned_date = models.DateField()
    completion_date = models.DateField(null=True, blank=True)
    certification = models.TextField(null=True, blank=True)
    score = models.DecimalField(max_digits=5, decimal_places=2, default=0.00)
    is_passed = models.BooleanField(default=False)
    feedback = models.TextField(null=True, blank=True)
    notes = models.TextField(null=True, blank=True)

    class Meta:
        db_table = 'assign_training'

    def __str__(self):
        return f"{self.employee.full_name if hasattr(self.employee, 'full_name') else 'Employee'} - {self.training_program.name}"