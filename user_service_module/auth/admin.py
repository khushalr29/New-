from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin 
from django.contrib.auth.models import Permission
from shared.models import (
    User, Role, UserActivityLog, Company, Plan, Subscription, 
    Employee, Department, Designation, Branch, CompanyType, 
    Holiday, DocumentType, AwardType, IndicatorCategory, Indicator, GoalType, 
    ReviewCycle, Resignations, Termination, Announcement, Assets, AssetType, 
    Award, Complaint, EmployeeGoal, EmployeeReview, Promotion, 
    TrainingType, TrainingProgram, TrainingSession, AssignTraining, 
    Transfer, Trip, Warning, CandidateAssessment, CandidateSource, Candidate, 
    ChecklistItem, CustomQuestions, InterviewType, InterviewRound, Interview, 
    InterviewFeedback, JobCategory, JobLocation, JobPosting, JobType, Offer, 
    OnboardingChecklist, Onboarding, PayrollRun, SalaryComponent, 
    LeaveType, LeaveApplication, LeaveBalance, LeavePolicy, 
    ActionItem, MeetingMinutes, MeetingRoom, MeetingAttendee, Meeting, MeetingType, 
    Shift, TimeEntries
)

# --- Base Admin with Multi-Tenancy Scoping ---

class HRMSModelAdmin(admin.ModelAdmin):
    def get_readonly_fields(self, request, obj=None):
        ro = super().get_readonly_fields(request, obj)
        # Check if model has audited fields
        opts = self.model._meta
        if any(f.name == 'created_at' for f in opts.fields):
            ro = list(ro) + ['created_at']
        if any(f.name == 'updated_at' for f in opts.fields):
            ro = list(ro) + ['updated_at']
        return ro
    
    def save_model(self, request, obj, form, change):
        if hasattr(obj, 'company') and not obj.company_id and not request.user.is_superuser:
            obj.company = request.user.company
        super().save_model(request, obj, form, change)

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if request.user.is_superuser or not hasattr(qs.model, 'company'):
            return qs
        return qs.filter(company=request.user.company)

# --- Core Admin ---

@admin.register(User)
class UserModelAdmin(BaseUserAdmin):
    list_display = ('id', 'email', 'full_name', 'company', 'account_type', 'is_staff')
    list_filter = ('company', 'account_type', 'status')
    readonly_fields = ('is_staff',)
    fieldsets = (
        ('User Credentials', {'fields': ('email', 'password')}),
        ('Personal Info', {'fields': ('full_name', 'gender', 'phone_number', 'company', 'account_type', 'status')}),
        ('Permissions', {'fields': ('is_enabled', 'is_staff', 'is_superuser', 'user_permissions')}),
        ('Roles', {'fields': ('roles',)})
    )
    search_fields = ('email', 'full_name')
    ordering = ('email',)
    filter_horizontal = ('user_permissions', 'roles')

@admin.register(Company)
class CompanyAdmin(HRMSModelAdmin):
    list_display = ('company_name', 'company_code', 'company_type', 'payment_status', 'created_at')
    search_fields = ('company_name', 'company_code')
    list_filter = ('company_type', 'payment_status')

@admin.register(Employee)
class EmployeeAdmin(HRMSModelAdmin):
    list_display = ('employee_id', 'full_name', 'company', 'designation', 'date_of_joining', 'status')
    search_fields = ('employee_id', 'full_name', 'email')
    list_filter = ('company', 'status', 'gender')

# --- HR Master Admin ---

@admin.register(Department)
class DepartmentAdmin(HRMSModelAdmin):
    list_display = ('department', 'unique_code', 'company', 'parent', 'status')
    list_filter = ('company', 'status')
    search_fields = ('department', 'unique_code')

@admin.register(Designation)
class DesignationAdmin(HRMSModelAdmin):
    list_display = ('name', 'department', 'company', 'status')
    list_filter = ('company', 'department', 'status')
    search_fields = ('name',)

@admin.register(Branch)
class BranchAdmin(HRMSModelAdmin):
    list_display = ('branch_name', 'city', 'company', 'status')
    list_filter = ('company', 'status')

# --- Recruitment Admin ---

@admin.register(JobPosting)
class JobPostingAdmin(HRMSModelAdmin):
    list_display = ('job_title', 'company', 'job_type', 'priority', 'is_featured_job')
    list_filter = ('company', 'job_type', 'priority')
    search_fields = ('job_title', 'job_description')

@admin.register(Candidate)
class CandidateAdmin(HRMSModelAdmin):
    list_display = ('candidate_fullname', 'email', 'job', 'candidate_status', 'source')
    list_filter = ('candidate_status', 'source', 'job__company')
    search_fields = ('candidate_fullname', 'email')

# --- Leave & Attendance Admin ---

@admin.register(LeaveApplication)
class LeaveApplicationAdmin(HRMSModelAdmin):
    list_display = ('employee', 'leave_type', 'start_date', 'end_date')
    list_filter = ('leave_type', 'company')

@admin.register(Shift)
class ShiftAdmin(HRMSModelAdmin):
    list_display = ('shift_name', 'start_time', 'end_time', 'company', 'status')
    list_filter = ('company', 'status')

# --- Payroll Admin ---

@admin.register(SalaryComponent)
class SalaryComponentAdmin(HRMSModelAdmin):
    list_display = ('name', 'component_type', 'calculation_type', 'fixed_amount', 'company')
    list_filter = ('company', 'component_type')

# --- Meetings & Operations ---

@admin.register(Meeting)
class MeetingAdmin(HRMSModelAdmin):
    list_display = ('title', 'organizer', 'meeting_date', 'start_time', 'end_time')
    list_filter = ('company', 'meeting_type')

@admin.register(UserActivityLog)
class UserActivityLogAdmin(admin.ModelAdmin):
    list_display = ('user', 'action', 'status', 'timestamp')
    list_filter = ('action', 'status', 'timestamp')
    readonly_fields = ('timestamp',)

# --- Generic Registration for Remaining Models ---

remaining_models = [
    Role, Permission, Plan, Subscription, CompanyType, 
    Holiday, DocumentType, AwardType, IndicatorCategory, Indicator, GoalType, 
    ReviewCycle, Resignations, Termination, Announcement, Assets, AssetType, 
    Award, Complaint, EmployeeGoal, EmployeeReview, Promotion, 
    TrainingType, TrainingProgram, TrainingSession, AssignTraining, 
    Transfer, Trip, Warning, CandidateAssessment, CandidateSource, 
    ChecklistItem, CustomQuestions, InterviewType, InterviewRound, Interview, 
    InterviewFeedback, JobCategory, JobLocation, JobType, Offer, 
    OnboardingChecklist, Onboarding, PayrollRun, LeaveType, LeaveBalance, LeavePolicy, 
    ActionItem, MeetingMinutes, MeetingRoom, MeetingAttendee, MeetingType, TimeEntries
]

for model in remaining_models:
    try:
        admin.site.register(model, HRMSModelAdmin)
    except admin.sites.AlreadyRegistered:
        pass

admin.site.site_header = "OKCare HRMS Admin"
admin.site.site_title = "HRMS Admin Portal"
admin.site.index_title = "Welcome to HRMS Dashboard"
