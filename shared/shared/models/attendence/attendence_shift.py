from django.db import models
from ..core.enums import CommonStatus

from ..core.base import TenantModel

class Shift(TenantModel):
    shift_name = models.CharField(max_length=255)
    start_time = models.TimeField()
    end_time = models.TimeField()
    break_duration = models.PositiveIntegerField(default=0)
    break_start_time = models.TimeField(null=True, blank=True)
    break_end_time = models.TimeField(null=True, blank=True)
    grade_period = models.PositiveIntegerField(default=0)
    is_night_shift = models.BooleanField(default=False)
    status = models.CharField(max_length=10, choices= CommonStatus.choices, default=CommonStatus.ACTIVE)

    class Meta:
        db_table = 'shift'
        unique_together = ('shift_name', 'start_time', 'end_time', 'company')
 
    def __str__(self):
        return f"{self.shift_name} ({self.start_time} - {self.end_time})"
    