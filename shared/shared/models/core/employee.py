import json
from django.db import models, IntegrityError
from django.utils import timezone
from django.contrib.auth.models import Permission
from ...utils.common import validate_char_field
from .enums import Gender, IdentityType, EmploymentType, EmployeeStatus
from .base import TenantModel

class EmployeeDesignation(TenantModel):
    employee = models.ForeignKey('shared.Employee', on_delete=models.CASCADE, related_name='employee_designations')
    designation = models.ForeignKey('shared.Designation', on_delete=models.CASCADE, related_name='employee_designations')
    effective_from = models.DateField()
    effective_to = models.DateField(null=True, blank=True)

    class Meta:
        db_table = 'employee_designation'
        ordering = ['-effective_from']

    def __str__(self):
        return f"{self.employee.full_name if hasattr(self.employee, 'full_name') else 'Employee'} -> {self.designation.title}"

class Employee(TenantModel):
    full_name = models.CharField(max_length=255, validators=[validate_char_field])
    employee_id = models.CharField(max_length=50, unique=True, db_index=True)
    employee_code = models.CharField(max_length=50, unique=True, db_index=True)
    personal_email_id = models.EmailField(max_length=255, unique=True)
    official_email_id = models.EmailField(max_length=255, unique=True)
    password = models.CharField(max_length=128) 
    date_of_birth = models.DateField(null=True, blank=True)
    profile_image = models.TextField(null=True, blank=True)
    gender = models.CharField(max_length=10, choices=Gender.choices)
    branch = models.ForeignKey('shared.Branch', on_delete=models.SET_NULL, null=True, blank=True, related_name='employees')
    department = models.ForeignKey('shared.Department', null=True, blank=True, on_delete=models.SET_NULL, related_name='employees')
    designation = models.ForeignKey('shared.EmployeeDesignation', null=True, blank=True, on_delete=models.SET_NULL, related_name='employees')
    date_of_joining = models.DateField(default=timezone.now)
    employment_type = models.CharField(max_length=20, choices=EmploymentType.choices, default=EmploymentType.FULL_TIME)
    shift = models.ForeignKey('shared.Shift', null=True, blank=True, on_delete=models.SET_NULL, related_name='employees')
    attendence_policy = models.ForeignKey('shared.AttendancePolicy', null=True, blank=True, on_delete=models.SET_NULL, related_name='employees')
    user_id = models.OneToOneField('shared.User', on_delete=models.CASCADE, related_name='employee_profile')
    manager = models.ForeignKey('self', null=True, blank=True, on_delete=models.SET_NULL, related_name='subordinates')
    identity_type = models.CharField(max_length=20, choices=IdentityType.choices, null=True, blank=True)
    identity_number = models.CharField(max_length=255, null=True, blank=True)
    employee_permissions = models.ManyToManyField(Permission,blank=True)
    address = models.CharField(max_length=255, null=True, blank=True)
    country_number_code = models.PositiveIntegerField(default=91)
    phone_number = models.CharField(max_length=20, blank=True)
    status = models.CharField(max_length=20, choices=EmployeeStatus.choices, default=EmployeeStatus.ACTIVE)
    bank_name = models.CharField(max_length=255, null=True, blank=True)
    account_holder_name = models.CharField(max_length=255, null=True, blank=True)
    bank_account_number = models.CharField(max_length=255, null=True, blank=True)
    bank_ifsc_code = models.CharField(max_length=255, null=True, blank=True)
    bank_branch_name = models.CharField(max_length=255, null=True, blank=True)
    tax_payer_id = models.CharField(max_length=255, null=True, blank=True)
    base_salary = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    emergency_contact_name = models.CharField(max_length=255, null=True, blank=True)
    emergency_contact_number = models.CharField(max_length=20, null=True, blank=True)
    emergency_contact_relationship = models.CharField(max_length=255, null=True, blank=True)
    resume = models.TextField(null=True, blank=True)
    created_by = models.ForeignKey('shared.User', on_delete=models.SET_NULL, null=True, blank=True, related_name='employees_created')
    updated_by = models.ForeignKey('shared.User', on_delete=models.SET_NULL, null=True, blank=True, related_name='employees_updated')
    deleted_by = models.ForeignKey('shared.User', on_delete=models.SET_NULL, null=True, blank=True, related_name='employees_deleted')

    class Meta:
        db_table = 'employee'
        ordering = ['full_name']
 
    def __str__(self):
        return f"{self.full_name} ({self.employee_code})"
 
    def _generate_employee_id(self):
        company_part = self.company.company_name[:4].upper() if self.company else "COMP"
        date_part = timezone.now().strftime("%Y%m%d")
        prefix = f"{company_part}-EMP-{date_part}-"
        
        last_emp = Employee.objects.filter(employee_id__startswith=prefix).order_by('-employee_id').first()
        if last_emp:
            try:
                last_seq = int(last_emp.employee_id.split('-')[-1])
                next_seq = last_seq + 1
            except (ValueError, IndexError):
                next_seq = 1
        else:
            next_seq = 1
            
        return f"{prefix}{next_seq:04d}"

    def clean(self):
        super().clean()
        if self.company and not self.id:
            employee_count = Employee.objects.filter(company=self.company).count()
            if hasattr(self.company, 'no_of_employees') and employee_count >= self.company.no_of_employees:
                 from django.core.exceptions import ValidationError
                 raise ValidationError("Company reached employee limit for the selected plan.")

    def save(self, *args, **kwargs):
        self.clean()
        if not self.employee_id:
            self.employee_id = self._generate_employee_id()
            if not self.employee_code:
                self.employee_code = self.employee_id
                
        try:
            return super().save(*args, **kwargs)
        except IntegrityError:
            if not kwargs.get('force_insert'):
                 self.employee_id = self._generate_employee_id()
                 self.employee_code = self.employee_id
                 return super().save(*args, **kwargs)
            raise

class EmployeeDocument(TenantModel):
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE, related_name='employee_documents')
    document_type = models.ForeignKey('shared.DocumentType', on_delete=models.CASCADE, related_name='employee_documents',null=True, blank=True)
    document_file = models.TextField(null=True, blank=True)
    
    class Meta:
        db_table = 'employee_document'
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.employee.full_name if hasattr(self.employee, 'full_name') else 'Employee'} -> {self.document_type.document_type}"