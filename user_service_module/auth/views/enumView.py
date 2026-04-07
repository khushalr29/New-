from rest_framework.views import APIView
from rest_framework.permissions import AllowAny
from shared.utils.response import ResponseHandler
from ..serializers.enumSerializer import (
    BillingModelSerializer, CoreModelSerializer, DependencyPermissionsSerializer, 
    PrintModelSerializer, SubscriptionModelSerializer, UploadCategorySerializers
)

from shared.models.core.enums import (
    Gender, MaritalStatus, PaymentMode, PaymentStatus, BillingChoice,
    Weekday, PriorityChoices, ExportImportFormat, AddsOnServices,
    ImageExtensions, DocumentExtensions, PurchaseOrderStatus, Status,
    Title, DispatchMethod, AgeFormat, AgeType, IdentityType, TransactionStatus,
    EmploymentType, EmployeeStatus, UserStatus, BranchStatus, CommonStatus,
    AttendancePolicy, PromotionStatus, GoalStatus, FrequencyEnum, ReviewStatus,
    TerminationType, WarningType, WarningSeverity, HolidayCategory, MeetingType,
    RecurrenceType, AttendanceStatus, AttendenceType, RSVPStatus, AccrualType,
    AnnouncementCategory, AssetStatus, AssetCondition, DepreciationMethod,
    TrainingStatus, MandatoryCategory, IconEnum, PayrollFrequencyEnum,
    ComponentType, CalculationType, RequiredType, JobApplicationType,
    CandidateStatus, RecommendationEnum, AssessmentEnum, SymbolPositionEnum,
    EmailProvider, SmtpEncryption, DocumentTemplateType, StorageDriver,
    CacheDriver, ButtonStyleEnum, LayoutStyleEnum, LanguageEnum, DateFormatEnum,
    TimeFormatEnum, TimeZone, SidebarVarientEnum, SidebarStyleEnum,
    LayoutDirectionEnum, ThemeModeEnum, DecimalSeparatorEnum,
    ThousandsSeparatorEnum, FileTypeEnum, ComplaintStatus, ComplaintType,
    AssignTrainingStatus, MeetingMinutesType
)

from ..enums import (
    BillingModels, SubscriptionModels, CoreModels,
    PrintAppModelS, UploadCategory, DependencyPermissions
)

class EnumListView(APIView):
    permission_classes = [AllowAny]
    
    def get(self, request):
        # Serialize local Auth Enums
        upload_category_data = {item['name']: item['value'] for item in UploadCategorySerializers(UploadCategory, many=True).data}
        subscription_data = {item['name']: item['value'] for item in SubscriptionModelSerializer(SubscriptionModels, many=True).data}
        billing_data = {item['name']: item['value'] for item in BillingModelSerializer(BillingModels, many=True).data}
        core_data = {item['name']: item['value'] for item in CoreModelSerializer(CoreModels, many=True).data}
        print_data = {item['name']: item['value'] for item in PrintModelSerializer(PrintAppModelS, many=True).data}
        permission_dependency_data = {item['name']: item['value'] for item in DependencyPermissionsSerializer(DependencyPermissions, many=True).data}

        response_data = {
            # Core & Identity
            "gender": dict(Gender.choices),
            "marital_status": dict(MaritalStatus.choices),
            "title": dict(Title.choices),
            "identity_type": dict(IdentityType.choices),
            "user_status": dict(UserStatus.choices),
            
            # HR & Employment
            "employment_type": dict(EmploymentType.choices),
            "employee_status": dict(EmployeeStatus.choices),
            "branch_status": dict(BranchStatus.choices),
            "common_status": dict(CommonStatus.choices),
            "attendance_policy": dict(AttendancePolicy.choices),
            
            # Performance & Ops
            "promotion_status": dict(PromotionStatus.choices),
            "goal_status": dict(GoalStatus.choices),
            "frequency": dict(FrequencyEnum.choices),
            "review_status": dict(ReviewStatus.choices),
            "termination_type": dict(TerminationType.choices),
            "warning_type": dict(WarningType.choices),
            "warning_severity": dict(WarningSeverity.choices),
            "complaint_status": dict(ComplaintStatus.choices),
            "complaint_type": dict(ComplaintType.choices),
            
            # Payroll
            "payroll_frequency": dict(PayrollFrequencyEnum.choices),
            "component_type": dict(ComponentType.choices),
            "calculation_type": dict(CalculationType.choices),
            "payment_mode": dict(PaymentMode.choices),
            "payment_status": dict(PaymentStatus.choices),
            
            # Recruitment
            "job_application_type": dict(JobApplicationType.choices),
            "candidate_status": dict(CandidateStatus.choices),
            "recommendation": dict(RecommendationEnum.choices),
            "assessment_status": dict(AssessmentEnum.choices),
            
            # Training & Assets
            "training_status": dict(TrainingStatus.choices),
            "assign_training_status": dict(AssignTrainingStatus.choices),
            "mandatory_category": dict(MandatoryCategory.choices),
            "asset_status": dict(AssetStatus.choices),
            "asset_condition": dict(AssetCondition.choices),
            
            # Meetings
            "meeting_type": dict(MeetingType.choices),
            "meeting_minutes_type": dict(MeetingMinutesType.choices),
            "rsvp_status": dict(RSVPStatus.choices),
            
            # Formats & Extensions
            "weekday": dict(Weekday.choices),
            "priority": dict(PriorityChoices.choices),
            "export_import_format": dict(ExportImportFormat.choices),
            "image_extensions": dict(ImageExtensions.choices),
            "document_extensions": dict(DocumentExtensions.choices),
            "date_format": dict(DateFormatEnum.choices),
            "time_format": dict(TimeFormatEnum.choices),
            "timezone": dict(TimeZone.choices),
            
            # System UI & Branding
            "theme_mode": dict(ThemeModeEnum.choices),
            "layout_direction": dict(LayoutDirectionEnum.choices),
            "sidebar_varient": dict(SidebarVarientEnum.choices),
            "sidebar_style": dict(SidebarStyleEnum.choices),
            "button_style": dict(ButtonStyleEnum.choices),
            "icons": dict(IconEnum.choices),
            
            # Auth Module Specific
            "upload_category": upload_category_data,
            "subscription_models": subscription_data,
            "billing_models": billing_data,
            "core_models": core_data,
            "print_models": print_data,
            "permission_dependencies": permission_dependency_data,
        }
        
        return ResponseHandler.list_success(response_data)
