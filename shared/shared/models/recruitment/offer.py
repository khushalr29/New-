from django.db import models
from .candidateSource import Candidate
from .jobPosting import JobPosting
from ..core.employee import Employee
from ..hr_management.hr_masters import Department   

from ..core.base import TenantModel

class Offer(TenantModel):
    candidate = models.ForeignKey(Candidate, on_delete=models.CASCADE, related_name='candidate_offer')
    position = models.ForeignKey(JobPosting, on_delete=models.CASCADE, related_name='position_offer')
    department = models.ForeignKey(Department, on_delete=models.CASCADE, related_name='dept_offer')
    salary = models.DecimalField(max_digits=15, decimal_places=2, default=0.00)
    start_date = models.DateField()
    expiration_date = models.DateField()
    approved_by = models.ForeignKey(Employee, on_delete=models.SET_NULL, null=True, related_name='approvedby_offer')
    benefits = models.TextField(null=True, blank=True)

    def __str__(self):
        return f"Offer for {self.candidate} - {self.position}"