import json
from django.db import models, IntegrityError
from django.utils import timezone
from ...utils.common import validate_char_field
from .enums import Gender, IdentityType, EmploymentType, EmployeeStatus, AttendancePolicy
from .base import TenantModel

class Employee(TenantModel):
    full_name = models.CharField(max_length=255, validators=[validate_char_field])
    employee_id = models.CharField(max_length=50, unique=True, db_index=True)
    employee_code = models.CharField(max_length=50, unique=True, db_index=True)
    email = models.EmailField(max_length=255, unique=True)
    password = models.CharField(max_length=128) 
    date_of_birth = models.DateField(null=True, blank=True)
    profile_image = models.TextField(null=True, blank=True)
    gender = models.CharField(max_length=10, choices=Gender.choices)
    branch = models.ForeignKey('shared.Branch', on_delete=models.SET_NULL, null=True, blank=True, related_name='employees')
    department = models.ForeignKey('shared.Department', null=True, blank=True, on_delete=models.SET_NULL, related_name='employees')
    designation = models.ForeignKey('shared.Designation', null=True, blank=True, on_delete=models.SET_NULL, related_name='employees')
    date_of_joining = models.DateField(default=timezone.now)
    employment_type = models.CharField(max_length=20, choices=EmploymentType.choices, default=EmploymentType.FULL_TIME)
    shift = models.ForeignKey('shared.Shift', null=True, blank=True, on_delete=models.SET_NULL, related_name='employees')
    attendence_policy = models.CharField(max_length=50, choices=AttendancePolicy.choices, default=AttendancePolicy.STANDARD_ATTENDANCE_POLICY)
    user = models.OneToOneField('shared.User', on_delete=models.CASCADE, related_name='employee_profile')
    manager = models.ForeignKey('self', null=True, blank=True, on_delete=models.SET_NULL, related_name='subordinates')
    identity_type = models.CharField(max_length=20, choices=IdentityType.choices, null=True, blank=True)
    identity_number = models.CharField(max_length=255, null=True, blank=True)
    address = models.CharField(max_length=255, null=True, blank=True)
    country_number_code = models.PositiveIntegerField(default=91)
    phone = models.CharField(max_length=20, blank=True)
    status = models.CharField(max_length=20, choices=EmployeeStatus.choices, default=EmployeeStatus.ACTIVE)
    
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
            # Simple retry for ID collision
            if not kwargs.get('force_insert'):
                 self.employee_id = self._generate_employee_id()
                 self.employee_code = self.employee_id
                 return super().save(*args, **kwargs)
            raise

class EmployeeDesignation(TenantModel):
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE, related_name='employee_designations')
    designation = models.ForeignKey('shared.Designation', on_delete=models.CASCADE, related_name='employee_designations')
    effective_from = models.DateField()
    effective_to = models.DateField(null=True, blank=True)
 
    class Meta:
        db_table = 'employee_designation'
        ordering = ['-effective_from']
 
    def __str__(self):
        return f"{self.employee.full_name if hasattr(self.employee, 'full_name') else 'Employee'} -> {self.designation.title}"
