from django.db import models
from ..core.enums import AnnouncementCategory
from ..core.base import TenantModel

class Announcement(TenantModel):
    title = models.CharField(max_length=255)
    category = models.CharField(max_length=20, choices=AnnouncementCategory.choices)
    short_description = models.TextField(null=True, blank=True)
    content = models.TextField()
    start_date = models.DateField()
    end_date = models.DateField()
    attachment = models.TextField(blank=True, null=True)
    is_featured_announcement = models.BooleanField(default=False)
    is_high_priority = models.BooleanField(default=False)
    is_company_wide_announcement = models.BooleanField(default=False)
    branch = models.ManyToManyField('shared.Branch', blank=True, related_name='announcements')
    department = models.ManyToManyField('shared.Department', blank=True, related_name='announcements')

    class Meta:
        db_table = 'announcement'
        ordering = ['-start_date']

    def __str__(self):
        return self.title