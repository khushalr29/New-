from django.db import models
from ..core.employee import Employee
from ..core.enums import ReviewStatus
from .hr_masters import ReviewCycle

from ..core.base import TenantModel

class EmployeeReview(TenantModel):
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE, related_name='employee_reviews')
    reviewer = models.ForeignKey(Employee, on_delete=models.SET_NULL, null=True, related_name='reviews_given')
    review_cycle = models.ForeignKey(ReviewCycle, on_delete=models.SET_NULL, null=True, related_name='employee_reviews')
    review_date = models.DateField()
    feedback = models.TextField(blank=True, null=True)
    rating = models.DecimalField(max_digits=3, decimal_places=2, null=True, blank=True)
    status = models.CharField(max_length=20, choices=ReviewStatus.choices, default=ReviewStatus.SCHEDULED)

    class Meta:
        db_table = 'employee_review'
        ordering = ['-review_date']