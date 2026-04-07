from django.db import models
from ..core.employee import Employee
from .hr_masters import GoalType
from ..core.enums import GoalStatus

from ..core.base import TenantModel

class EmployeeGoal(TenantModel):
    employee = models.ForeignKey('shared.Employee', on_delete=models.CASCADE, related_name='employee_goals')
    goal_type = models.ForeignKey(GoalType, on_delete=models.SET_NULL, null=True, related_name='employee_goals')
    goal_title = models.CharField(max_length=255, null=True, blank=True)
    description = models.TextField(blank=True, null=True)
    start_date = models.DateField()
    end_date = models.DateField()
    target = models.CharField(max_length=50, blank=True, null=True)
    progress_percentage = models.DecimalField(max_digits=5, decimal_places=2, default=0.00) 
    status = models.CharField(max_length=20, choices=GoalStatus.choices, default=GoalStatus.PENDING)

    class Meta:
        db_table = 'employee_goal'
        ordering = ['-start_date']

    def __str__(self):
        return f"{self.employee.full_name} - {self.goal_title}"