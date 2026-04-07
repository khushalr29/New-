from django.db import models
from .jobType import JobType
from .jobLocation import JobLocation
from .customQuestions import CustomQuestions
from ..hr_management.hr_masters import Branch, Department
from ..core.enums import PriorityChoices, JobApplicationType

from ..core.base import TenantModel

class JobPosting(TenantModel):
    job_title = models.CharField(max_length=255)
    job_type = models.ForeignKey(JobType, on_delete=models.CASCADE, related_name='job_postings')
    location = models.ForeignKey(JobLocation, on_delete=models.CASCADE, related_name='job_postings')
    branch = models.ForeignKey(Branch , on_delete=models.CASCADE, related_name='job_postings')
    department = models.ForeignKey(Department , on_delete=models.CASCADE, related_name='job_postings')
    priority = models.CharField(max_length=10, choices=PriorityChoices.choices, default=PriorityChoices.LOW)
    required_skills = models.CharField(max_length=255)
    start_date = models.DateField()
    application_deadline = models.DateField()
    job_application = models.CharField(max_length=20, choices=JobApplicationType.choices, default=JobApplicationType.EXISTING_LINK)
    application_url = models.TextField()
    no_of_position = models.PositiveIntegerField(default=1)
    is_featured_job = models.BooleanField(default=False)
    min_experience = models.PositiveIntegerField(default=0)
    max_experience = models.PositiveIntegerField(default=1)
    min_salary = models.PositiveIntegerField(default=0)
    max_salary = models.PositiveIntegerField(default=0)
    job_description = models.TextField()
    responsibilities = models.TextField()
    qualification = models.TextField()
    education = models.TextField()
    benefits = models.TextField()
    custom_questions = models.ManyToManyField(CustomQuestions, blank=True, related_name='job_postings')
    is_gender = models.BooleanField(default=False)
    is_dob = models.BooleanField(default=False)
    is_cover_letter = models.BooleanField(default=False)
    is_terms_and_condition = models.BooleanField(default=False)

    class Meta:
        db_table = 'job_posting'
        ordering = ['-created_at']

    def __str__(self):
        return self.job_title