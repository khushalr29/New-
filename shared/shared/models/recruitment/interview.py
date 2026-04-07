from django.db import models
from ..core.enums import CommonStatus, RecommendationEnum
from .jobPosting import JobPosting
from .candidateSource import Candidate
from ..core.employee import Employee

class InterviewType(models.Model):
    interview_type_name = models.CharField(max_length=255)
    description = models.TextField(null=True, blank=True)
    status = models.CharField(max_length=20, choices=CommonStatus.choices, default=CommonStatus.ACTIVE)
    created_at = models.DateTimeField(null=True, blank=True)
    updated_at = models.DateTimeField(null=True, blank=True)
    deleted_at = models.DateTimeField(null=True, blank=True)

class InterviewRound(models.Model):
    job = models.ForeignKey(JobPosting, on_delete=models.CASCADE, related_name='interview_round')
    name = models.CharField(max_length=255)
    sequence_no = models.PositiveIntegerField(default=1)
    description = models.TextField(null=True, blank=True)
    status = models.CharField(max_length=255, choices=CommonStatus.choices, default=CommonStatus.ACTIVE)
    created_at = models.DateTimeField(null=True, blank=True)
    updated_at = models.DateTimeField(null=True, blank=True)
    deleted_at = models.DateTimeField(null=True, blank=True)

class Interview(models.Model):
    candidate = models.ForeignKey(Candidate, on_delete=models.CASCADE, related_name='candidate_interview')
    round  = models.ForeignKey(InterviewRound, on_delete=models.CASCADE, related_name='candidate_round')
    interview_type = models.ForeignKey(InterviewType, on_delete=models.CASCADE, related_name='interview_type')
    date = models.DateField()
    time = models.TimeField()
    duration = models.PositiveIntegerField(default=0)
    location = models.CharField(max_length=255, null=True, blank=True)
    meeting_link = models.TextField(null=True, blank=True)
    interviewer = models.ManyToManyField(Employee,blank=True, related_name='interviewer')
    created_at = models.DateTimeField(null=True, blank=True)
    updated_at = models.DateTimeField(null=True, blank=True)
    deleted_at = models.DateTimeField(null=True, blank=True)

class InterviewFeedback(models.Model):
    interview = models.ForeignKey(Interview, on_delete=models.CASCADE, related_name='interview_feedback')
    technical_rating = models.DecimalField(max_digits=2, decimal_places=1, default=0.0)
    communication_rating = models.DecimalField(max_digits=2, decimal_places=1, default=0.0)
    cultural_fit_rating = models.DecimalField(max_digits=2, decimal_places=1, default=0.0)
    overall_rating = models.DecimalField(max_digits=2, decimal_places=1, default=0.0)
    recommendation = models.CharField(max_length=25, choices = RecommendationEnum.choices)
    strength = models.TextField(null=True, blank=True)
    weakness = models.TextField(null=True, blank=True)
    comments = models.TextField(null=True, blank=True)
    created_at = models.DateTimeField(null=True, blank=True)
    updated_at = models.DateTimeField(null=True, blank=True)
    deleted_at = models.DateTimeField(null=True, blank=True)
    

