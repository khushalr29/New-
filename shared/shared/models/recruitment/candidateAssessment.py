from django.db import models
from .candidateSource import Candidate
from ..core.enums import AssessmentEnum
from ..core.base import TenantModel

class CandidateAssessment(TenantModel):
    candidate = models.ForeignKey(Candidate, on_delete=models.CASCADE, related_name='assessments')
    assessment_name = models.CharField(max_length=255, blank=True, null=True)
    score = models.DecimalField(max_digits=5, decimal_places=2, default=0.00)
    max_score = models.DecimalField(max_digits=5, decimal_places=2, default=100.00)
    status = models.CharField(max_length=20, choices=AssessmentEnum.choices, default=AssessmentEnum.PENDING)
    conducted_by = models.ForeignKey('shared.Employee', on_delete=models.SET_NULL, null=True, blank=True, related_name='assessments_conducted')
    assessment_date = models.DateField()
    comments = models.TextField(null=True, blank=True)

    class Meta:
        db_table = 'candidate_assessment'

    def __str__(self):
        return f"{self.assessment_name} - {self.status}"
