from django.db import models
from shared.utils.common import validate_name, validate_address, validate_char_field,validate_phone_number
from ..core.enums import BranchStatus, DocStatus, FrequencyEnum, TerminationType, HolidayCategory
from ..core.base import BaseModel, TenantModel

def get_default_company():
    from ..core.company import Company
    company = Company.objects.first()
    return company.id if company else None

def generate_unique_code():
    import uuid
    return f"DEPT-{uuid.uuid4().hex[:6].upper()}"



class CompanyType(BaseModel):
    company_type = models.CharField(max_length=100,validators=[validate_name])
    description= models.TextField(blank = True,validators=[validate_address])

    def __str__(self):
        return self.company_type

class Department(TenantModel):
    department = models.CharField(max_length=255)
    branch = models.ForeignKey('shared.Branch', on_delete=models.CASCADE, related_name='departments')
    description = models.TextField(blank=True, null=True)
    unique_code = models.CharField(max_length=255, unique=True)
    parent = models.ForeignKey('self', null=True, blank=True,
    on_delete=models.SET_NULL, related_name='sub_departments')
    status = models.CharField(max_length=10, choices= BranchStatus.choices, default=BranchStatus.ACTIVE)
    created_by = models.ForeignKey('shared.User', on_delete=models.SET_NULL, null=True, blank=True, related_name='departments_created')

    class Meta:
        db_table = 'department'
        unique_together = ('unique_code', 'department', 'company')
 
    def __str__(self):
        return f"{self.department} — {self.unique_code}"
    
class Branch(TenantModel):
    branch_name = models.CharField(max_length=255, validators=[validate_char_field])
    branch_code = models.CharField(max_length=255, unique=True)
    address = models.TextField(blank=True, null=True, validators=[validate_address])
    city = models.CharField(max_length=100, validators=[validate_char_field])
    state = models.CharField(max_length=100, validators=[validate_char_field])
    zip_code = models.CharField(max_length=20, validators=[validate_char_field])
    country_code_number = models.CharField(max_length=5)
    phone_number = models.CharField(max_length=15, validators=[validate_phone_number])
    email = models.EmailField(max_length=255, null=True, blank=True)
    status = models.CharField(max_length=10, choices= BranchStatus.choices, default=BranchStatus.ACTIVE)
    created_by = models.ForeignKey('shared.User', on_delete=models.SET_NULL, null=True, blank=True, related_name='branches_created')

    class Meta:
        db_table = 'branch'
        unique_together = ('branch_name', 'phone_number', 'company')
  
    def __str__(self):
        return f"{self.branch_name} — {self.city}"

class DocumentType(TenantModel):
    document_type = models.CharField(max_length=100, validators=[validate_name])
    description = models.TextField(blank=True, null=True)
    status = models.CharField(max_length=10, choices= DocStatus.choices, default=DocStatus.REQUIRED)

    class Meta:
        db_table = 'document_type'
        unique_together = ('document_type', 'company')

    def __str__(self):
        return self.document_type    

class AwardType(TenantModel):
    award_type = models.CharField(max_length=100, validators=[validate_name])
    description = models.TextField(blank=True, null=True)
    status = models.CharField(max_length=10, choices= BranchStatus.choices, default=BranchStatus.ACTIVE)

    class Meta:
        db_table = 'award_type'
        unique_together = ('award_type', 'company')

    def __str__(self):
        return self.award_type

class Designation(TenantModel):
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    department = models.ForeignKey(Department, on_delete=models.CASCADE, related_name='designations')
    level = models.CharField(max_length=50, blank=True, help_text="e.g. Junior, Senior, Lead, Manager")
    status = models.CharField(max_length=20, choices=BranchStatus.choices, default=BranchStatus.ACTIVE)
 
    class Meta:
        db_table = 'designation'
        unique_together = ('title', 'company')
 
    def __str__(self):
        return f"{self.title} ({self.level})"

class IndicatorCategory(TenantModel):
    category_name = models.CharField(max_length=255, validators=[validate_char_field])
    description = models.TextField(blank=True, null=True)
    status = models.CharField(max_length=20, choices=BranchStatus.choices, default=BranchStatus.ACTIVE)

    class Meta:
        db_table = 'indicator_category'
        unique_together = ('category_name', 'company')
 
    def __str__(self):
        return self.category_name

class Indicator(TenantModel):
    indicator_name = models.CharField(max_length=255, validators=[validate_char_field])
    category = models.ForeignKey(IndicatorCategory, on_delete=models.CASCADE, related_name='indicators')
    description = models.TextField(blank=True, null=True)
    measurement_unit = models.CharField(max_length=50, blank=True, null=True)
    target_value = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    status = models.CharField(max_length=20, choices=BranchStatus.choices, default=BranchStatus.ACTIVE)

    class Meta:
        db_table = 'indicator'
        unique_together = ('category', 'indicator_name', 'company')
 
    def __str__(self):
        return f"{self.indicator_name} ({self.category.category_name})"

class GoalType(TenantModel):
    goal_name = models.CharField(max_length=255, validators=[validate_char_field])
    description = models.TextField(blank=True, null=True)
    status = models.CharField(max_length=20, choices=BranchStatus.choices, default=BranchStatus.ACTIVE)

    class Meta:
        db_table = 'goal'
        unique_together = ('goal_name', 'company')
 
    def __str__(self):
        return self.goal_name

class ReviewCycle(TenantModel):
    cycle_name = models.CharField(max_length=255, validators=[validate_char_field])
    frequency = models.CharField(max_length=20, choices=FrequencyEnum.choices, default=FrequencyEnum.ANNUAL)
    description = models.TextField(blank=True, null=True)
    start_date = models.DateField()
    end_date = models.DateField()
    status = models.CharField(max_length=20, choices=BranchStatus.choices, default=BranchStatus.ACTIVE)

    class Meta:
        db_table = 'review_cycle'
        unique_together = ('cycle_name', 'company')
 
    def __str__(self):
        return self.cycle_name

class Resignations(TenantModel):
    employee = models.ForeignKey('Employee', on_delete=models.CASCADE, related_name='resignations')
    resignation_date = models.DateField()
    last_working_day = models.DateField()
    notice_period = models.CharField(max_length=50, blank=True, null=True)
    resignation_reason = models.CharField(max_length=255, validators=[validate_char_field])
    description = models.TextField(blank=True, null=True)
    document = models.TextField(blank=True, null=True)
    status = models.CharField(max_length=20, choices=BranchStatus.choices, default=BranchStatus.ACTIVE)

    class Meta:
        db_table = 'resignation_reason'
        unique_together = ('resignation_reason', 'company')
 
    def __str__(self):
        return self.resignation_reason

class Termination(TenantModel):
    employee = models.ForeignKey('Employee', on_delete=models.CASCADE, related_name='terminations')
    termination_type = models.CharField(max_length=50,choices=TerminationType.choices, default=TerminationType.VOLUNTARY)
    termination_date = models.DateField()
    last_working_day = models.DateField()
    termination_reason = models.CharField(max_length=255, validators=[validate_char_field])
    description = models.TextField(blank=True, null=True)
    document = models.TextField(blank=True, null=True)
    status = models.CharField(max_length=20, choices=BranchStatus.choices, default=BranchStatus.ACTIVE)

    class Meta:
        db_table = 'termination_reason'
        unique_together = ('termination_reason', 'company')
 
    def __str__(self):
        return self.termination_reason

class Holiday(TenantModel):
    holiday_name = models.CharField(max_length=255, validators=[validate_char_field])
    category = models.CharField(max_length=20, choices = HolidayCategory.choices, default=HolidayCategory.NATIONAL)
    start_date = models.DateField()
    end_date = models.DateField()
    description = models.TextField(blank=True, null=True)
    is_paid_holiday = models.BooleanField(default=False)
    is_half_day = models.BooleanField(default=False)
    applicable_branches = models.ManyToManyField(Branch, related_name='holidays', blank=True)
    status = models.CharField(max_length=20, choices=BranchStatus.choices, default=BranchStatus.ACTIVE)

    class Meta:
        db_table = 'holiday'
        unique_together = ('holiday_name', 'start_date', 'company')
 
    def __str__(self):
        return f"{self.holiday_name} on {self.start_date}"