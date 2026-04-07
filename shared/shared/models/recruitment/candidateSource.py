from django.db import models
from ..core.enums import CommonStatus
from .jobPosting import JobPosting
from ..core.enums import Gender, CandidateStatus
from ..core.static import Country,City,State

from ..core.base import TenantModel

class CandidateSource(TenantModel):
    source_name = models.CharField(max_length=255)
    description = models.TextField(null=True,blank=True)
    status = models.CharField(max_length=20, choices=CommonStatus.choices, default=CommonStatus.ACTIVE)

class Candidate(TenantModel):
    candidate_fullname = models.CharField(max_length=255)
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=15)
    gender = models.CharField(max_length=10, choices=Gender.choices, null=True, blank=True)
    dob = models.DateField(null=True, blank=True)
    resume = models.TextField()
    cover_letter = models.TextField()
    source = models.ForeignKey(CandidateSource,on_delete=models.SET_NULL,null=True, blank=True,related_name='candidates')
    job = models.ForeignKey(JobPosting, on_delete=models.CASCADE, related_name='candidates')
    experience = models.CharField(max_length=50)
    current_salary = models.CharField(max_length=255)
    expected_salary = models.CharField(max_length=255)
    is_any_disability = models.BooleanField(default=False)
    disability = models.TextField(null=True, blank=True)
    candidate_status = models.CharField(max_length=50, choices=CandidateStatus.choices, default=CandidateStatus.APPLIED)
    corresponding_address = models.TextField()
    permanent_address = models.TextField()
    country = models.ForeignKey(Country, on_delete=models.CASCADE, related_name='candidates')
    state = models.ForeignKey(State, on_delete=models.CASCADE, related_name='candidates')
    city = models.ForeignKey(City, on_delete=models.CASCADE,related_name='candidates')
    pincode = models.CharField(max_length=255)
    is_work_before = models.BooleanField(default =False)
    known_languages = models.CharField(max_length=255)
    website = models.TextField()
    all_information_correct = models.BooleanField(default=False)

    def __str__(self):
        return self.candidate_fullname
 
