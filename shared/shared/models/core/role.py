from django.db import models
from shared.utils.common import validate_name
from django.contrib.auth.models import Permission

from .base import TenantModel

class Role(TenantModel):
    name = models.CharField(max_length=150, validators=[validate_name])
    description = models.TextField(blank=True, null=True)
    permissions = models.ManyToManyField(Permission, blank=True)
    
    class Meta:
        db_table = 'role'
        unique_together = ('name', 'company')
    
    def __str__(self):
        return f"{self.name}"