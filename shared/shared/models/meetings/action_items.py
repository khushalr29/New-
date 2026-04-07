from django.db import models
from .meetings import Meeting
from ..core.employee import Employee
from ..core.enums import PriorityChoices

class ActionItem(models.Model):
    meeting = models.ForeignKey(Meeting, on_delete=models.CASCADE, related_name='action_items')
    action_item_title = models.CharField(max_length=255)
    description = models.TextField()
    assigned_to = models.ForeignKey(Employee, on_delete=models.SET_NULL, null=True, related_name='assigned_action_items')
    due_date = models.DateField()
    priority = models.CharField(max_length=20, choices=PriorityChoices.choices)
    progress = models.PositiveIntegerField(default=0)
    notes = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(null=True, blank=True)
    updated_at = models.DateTimeField(null=True, blank=True)
    deleted_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        db_table = 'action_item'
        ordering = ['due_date']

    def __str__(self):
        return f"{self.description} - {self.status}"