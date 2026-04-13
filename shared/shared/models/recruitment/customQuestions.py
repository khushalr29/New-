from django.db import models
from ..core.enums import RequiredType
from ..core.base import TenantModel

class CustomQuestions(TenantModel):
    question = models.CharField(max_length=255)
    required = models.CharField(max_length=3, choices=RequiredType.choices, default=RequiredType.NO)

    class Meta:
        db_table = 'custom_questions'

    def __str__(self):  
        return self.question
