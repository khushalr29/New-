from django.db import models
from ..core.enums import CommonStatus, IconEnum, MandatoryCategory

from ..core.base import TenantModel

class DocumentCategories(TenantModel):
    category_name = models.CharField(max_length=255)
    description = models.TextField(null=True, blank=True)
    color = models.CharField(max_length=7)
    icon = models.CharField(max_length=20, choices=IconEnum.choices, default=IconEnum.FOLDER)
    mandatory_category = models.CharField(max_length=20, choices=MandatoryCategory.choices, default=MandatoryCategory.NO_OPTIONAL)
    status = models.CharField(max_length=20, choices= CommonStatus.choices)
    
    def __str__(self):
        return self.category_name