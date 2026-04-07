from django.db import models

class CalenderSchedule(models.Model):
    date = models.DateField()
    event_name = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(null=True, blank=True)
    updated_at = models.DateTimeField(null=True, blank=True)
    deleted_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        db_table = 'calender_schedule'
        unique_together = ('date', 'event_name')


    def __str__(self):
        return f"{self.event_name} - {self.date}"