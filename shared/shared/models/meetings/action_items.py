from django.db import models
from .meetings import Meeting
from ..core.employee import Employee
from ..core.enums import PriorityChoices, CommonStatus
from ..core.base import TenantModel

class ActionItem(TenantModel):
    meeting = models.ForeignKey(Meeting, on_delete=models.CASCADE, related_name='action_items')
    action_item_title = models.CharField(max_length=255)
    description = models.TextField()
    assigned_to = models.ForeignKey(Employee, on_delete=models.SET_NULL, null=True, related_name='assigned_action_items')
    due_date = models.DateField()
    priority = models.CharField(max_length=20, choices=PriorityChoices.choices)
    progress = models.PositiveIntegerField(default=0)
    status = models.CharField(max_length=20, choices=CommonStatus.choices, default=CommonStatus.ACTIVE)
    notes = models.TextField(blank=True, null=True)

    class Meta:
        db_table = 'action_item'
        ordering = ['due_date']
        unique_together = ('action_item_title', 'meeting', 'company')

    def __str__(self):
        return f"{self.action_item_title} - {self.status}"