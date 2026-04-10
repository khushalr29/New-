from django.db import models

class Gender(models.TextChoices):
    MALE =  "Male"
    FEMALE = "Female"
    OTHER = "Other"

class MaritalStatus(models.TextChoices):
    SINGLE = "Single"
    MARRIED = "Married"
    DIVORCED = "Divorced"
    WIDOWED = "Widowed"
    SEPARATED = "Separated"

class PaymentMode(models.TextChoices):
    CASH = "Cash"
    ONLINE = "Online"
    UPI = 'UPI'
    CARD = 'Card'

class PaymentStatus(models.TextChoices):
    PENDING = 'Pending'
    PAID = 'Paid'
    OVERDUE = 'Overdue'
    CANCELLED = 'Cancelled'

class BillingChoice(models.TextChoices):
    MONTHLY = "Monthly"
    QUARTERLY = "Quarterly"
    YEARLY = "Yearly"
    
class Weekday(models.TextChoices):
    MONDAY = "Monday"
    TUESDAY = "Tuesday"
    WEDNESDAY = "Wednesday"
    THURSDAY = "Thursday"
    FRIDAY = "Friday"
    SATURDAY = "Saturday"
    SUNDAY = "Sunday"

class PriorityChoices(models.TextChoices):
    HIGH = 'High'
    MEDIUM = 'Medium'
    LOW = 'Low'

class SessionStatus(models.TextChoices):
    SCHEDULED = 'Scheduled'
    COMPLETED = 'Completed'
    CANCELLED = 'Cancelled'
    IN_PROGRESS = 'In Progress'
    RESCHEDULE = 'Reschedule'

class ExportImportFormat(models.TextChoices):
    CSV = 'csv'
    XLS = 'xls'
    XLSX = 'xlsx'
    JSON = 'json'
    YAML = 'yaml'
    ODS = 'ods'

class AddsOnServices(models.TextChoices):
    EMAIL = "Email"
    SMS = "sms"
    IVR = "ivr"

class ImageExtensions(models.TextChoices):
    PNG = "png"
    JPEG = "jpeg"
    JPG = "jpg"
    SVG = "svg"
    WEBP = "webp"

class DocumentExtensions(models.TextChoices):
    PDF = "pdf"
    DOC = "doc"
    DOCX = "docx"
    CSV = "csv"
    XLSX = "xlsx"

class PurchaseOrderStatus(models.TextChoices):
    PENDING = "Pending"
    COMPLETE = "Complete"
    PARTIALLY_PAID = "Partially Paid"
    PARTIALLY_FULLFILLED = "Partially Fulfilled"

class Status(models.TextChoices):
    PENDING = 'Pending'
    APPROVED = 'Approved'
    PARTIALLY_FULFILLED = 'Partially Fulfilled'
    FULFILLED = 'Fulfilled'
    CANCELLED = 'Cancelled'
    REJECTED = 'Rejected'

class Title(models.TextChoices):
    MR ="MR."
    MRS ="MRS."
    SHRI ="SHRI."
    MS ="MS."
    MASTER ="MASTER."
    MISS ="MISS."
    SMT ="SMT."
    DR ="DR."
    KUMAR ="KUMAR."
    KUMARI ="KUMARI."
    MOHD ="MOHD."
    BABY_OR_JUST_BORN="BABY OR JUST BORN"
    BABY="BABY"
    BABY_OF="BABY OF"
    PET_OF="PET OF"
    S_O="S/O"
    D_O="D/O"
    C_O="C/O"
    M_O="M/O"
    BLANK="BLANK"

class DispatchMethod(models.TextChoices):
    SMS =  "SMS"
    EMAIL = "Email"
    WHATSAPP = "Whatsapp"
    HARDCOPY = "Hardcopy"
    MANUAL_WHATSAPP = "Manual Whatsapp"

class AgeFormat(models.TextChoices):
    YEARS_ONLY = "Year Only"
    YEARS_MONTHs_DAYS = "Years-Months-Days(Y-M-D)"

class AgeType(models.TextChoices):
    YEARS = "Years"
    MONTHS = "Months"
    DAYS = "Days"

class IdentityType(models.TextChoices):
    AADHAAR = "Aadhaar"
    PASSPORT = "Passport"
    DRIVING_LICENSE = "Driving License"
    VOTER_ID = "Voter ID"
    PAN_CARD = "PAN Card"
    NATIONAL_ID = "National ID"
    SOCIAL_SECURITY_NUMBER = "SSN"
    HEALTH_ID = "Health ID"

class TransactionStatus(models.TextChoices):
    TRANSACTION_FAILED ="Transaction Failed"
    TRANSACTION_SUCCESSFULLY = "Transaction Successfully"

class EmploymentType(models.TextChoices):
    FULL_TIME = 'full_time', 'Full Time'
    PART_TIME = 'part_time', 'Part Time'
    CONTRACT = 'contract', 'Contract'
    INTERN = 'intern', 'Intern'
 
class EmployeeStatus(models.TextChoices):
    ACTIVE = 'active', 'Active'
    INACTIVE = 'inactive', 'Inactive'
    ON_LEAVE = 'on_leave', 'On Leave'
    TERMINATED = 'terminated', 'Terminated'

class UserStatus(models.TextChoices):
    ACTIVE = 'active', 'Active'
    INACTIVE = 'inactive', 'Inactive'
    SUSPENDED = 'suspended', 'Suspended'
    DELETED = 'deleted', 'Deleted'

class BranchStatus(models.TextChoices):
    ACTIVE = 'active', 'Active'
    INACTIVE = 'inactive', 'Inactive'
    CLOSED = 'closed', 'Closed'

class CommonStatus(models.TextChoices):
    ACTIVE = 'active', 'Active'
    INACTIVE = 'inactive', 'Inactive'

class DocStatus(models.TextChoices):
    REQUIRED= 'required', 'Required'
    OPTIONAL = 'optional', 'Optional'

class AttendancePolicy(models.TextChoices):
    STANDARD_ATTENDANCE_POLICY = 'standard_attendance_policy', 'Standard Attendance Policy'
    FLEXIBLE_ATTENDANCE_POLICY = 'flexible_attendance_policy', 'Flexible Attendance Policy'
    STRICT_ATTENDANCE_POLICY = 'strict_attendance_policy', 'Strict Attendance Policy'

class PromotionStatus(models.TextChoices):
    PENDING = 'pending', 'Pending'
    APPROVED = 'approved', 'Approved'
    REJECTED = 'rejected', 'Rejected'

class GoalStatus(models.TextChoices):
    PENDING = 'pending', 'Pending'
    IN_PROGRESS = 'in_progress', 'In Progress'
    COMPLETED = 'completed', 'Completed'
    CANCELLED = 'cancelled', 'Cancelled'

class FrequencyEnum(models.TextChoices):
    SEMIANNUAL = 'semi-annual', 'Semi-Annual'
    DAILY = 'daily', 'Daily'
    WEEKLY = 'weekly', 'Weekly'
    MONTHLY = 'monthly', 'Monthly'
    QUARTERLY = 'quarterly', 'Quarterly'
    ANNUAL = 'annual', 'Annual'

class ReviewStatus(models.TextChoices):
    SCHEDULED = 'scheduled', 'Scheduled'
    INPROGRESS = 'in_progress', 'In Progress'

class TerminationType(models.TextChoices):
    VOLUNTARY = 'voluntary', 'Voluntary'
    INVOLUNTARY = 'involuntary', 'Involuntary'
    RETIREMENT = 'retirement', 'Retirement'
    LAYOFF = 'layoff', 'Layoff'
    CONTRACT_COMMPLETION = 'contract_completion', 'Contract Completion'
    PROBATION_FAILURE = 'probation_failure', 'Probation Failure'
    MISCONDUCT = 'misconduct', 'Misconduct'
    PERFORMANCE_ISSUES = 'performance_issues', 'Performance Issues'

class WarningType(models.TextChoices):
    ATTENDENCE = 'attendence', 'Attendence'
    PERFORMANCE = 'performance', 'Performance'
    CONDUCT = 'conduct', 'Conduct'
    POLICY_VIOLATION = 'policy_violation', 'Policy Violation'
    SAFETY = 'safety', 'Safety'
    COMMUNICATION = 'communication', 'Communication'
    INSUBORDINATION = 'insubordination', 'Insubordination'
    CONFIDENTIALITY = 'confidentiality', 'Confidentiality'

class WarningSeverity(models.TextChoices):
    VERBAL = 'verbal', 'Verbal'
    WRITTEN = 'written', 'Written'
    FINAL = 'final', 'Final'

class HolidayCategory(models.TextChoices):
    NATIONAL = 'national', 'National'
    RELIGIOUS = 'religious', 'Religious'
    SEASONAL = 'seasonal', 'Seasonal'
    COMPANY_SPECIFIC = 'company_specific', 'Company Specific'
    OTHER = 'other', 'Other'

class MeetingType(models.TextChoices):
    VIRTUAL = 'virtual', 'Virtual'
    PHYSICAL = 'physical', 'Physical'

class RecurrenceType(models.TextChoices):
    DAILY = 'daily', 'Daily'
    WEEKLY = 'weekly', 'Weekly'
    MONTHLY = 'monthly', 'Monthly'
    YEARLY = 'yearly', 'Yearly'

class AttendanceStatus(models.TextChoices):
    NOT_ATTENDED = 'not_attended', 'Not Attended'
    PRESENT = 'present', 'Present'
    LATE = 'late', 'Late'
    LEFT_EARLY = 'left_early', 'Left Early'

class AttendenceType(models.TextChoices):
    REQUIRED = 'required', 'Required'
    OPTIONAL = 'optional', 'Optional'

class RSVPStatus(models.TextChoices):
    ACCEPTED = 'accepted', 'Accepted'
    DECLINED = 'declined', 'Declined'
    TENTATIVE = 'tentative', 'Tentative'
    PENDING = 'pending', 'Pending'

class AccrualType(models.TextChoices):
    YEARLY = 'yearly', 'Yearly'
    MONTHLY = 'monthly', 'Monthly'

class AnnouncementCategory(models.TextChoices):
    GENERAL = 'general', 'General'
    HR = 'hr', 'HR'
    IT_UPDATES = 'it_updates', 'IT Updates'
    EVENTS = 'events', 'Events'
    POLICY_UPDATES = 'policy_updates', 'Policy Updates'
    COMPANY_NEWS = 'company_news', 'Company News'

class AssetStatus(models.TextChoices):
    ASSIGNED = 'assigned', 'Assigned'
    AVAILABLE = 'available', 'Available'
    UNDER_MAINTENANCE = 'under_maintenance', 'Under Maintenance'
    DISPOSED = 'disposed', 'Disposed'

class AssetCondition(models.TextChoices):
    NEW = 'new', 'New'
    GOOD = 'good', 'Good'
    FAIR = 'fair', 'Fair'
    POOR = 'poor', 'Poor'

class DepreciationMethod(models.TextChoices):
    STRAIGHT_LINE = 'straight_line', 'Straight Line'
    REDUCING_BALANCE = 'reducing_balance', 'Reducing Balance'
    NO_DEPRECIATION = 'no_depreciation', 'No Depreciation'

class TrainingStatus(models.TextChoices):
    DRAFT = 'Draft','draft'
    COMPLETED = 'Completed','completed'
    ACTIVE = 'Active','active'
    CANCELLED = 'Cancelled','cancelled'

class MandatoryCategory(models.TextChoices):
    NO_OPTIONAL = 'No, Optional','no, optional'
    YES_MANDATORY = 'Yes, Mandatory','yes, mandatory'

class IconEnum(models.TextChoices):
    IDCARD='Id Card', 'id card'
    GRADUATIONCAP='Graduation Cap','graduation cap'
    BRIEFCASE ='Brief Case','brief case'
    DOLLARSIGN = 'Dollar Sign', 'dollar sign'
    HEART = 'Heart','heart'
    SCALE='Scale','scale'
    AWARD = 'Award','award'
    TRENDING_UP = 'Trending Up','trending up'
    USER = 'User','user'
    SHIELD ='Shield','shield'
    FILETEXT = 'File Text','file text'
    FOLDER = 'Folder','folder'
    BOOK ='Book','book'
    CLIPBOARD_LIST = 'Clipboard List','clipboard list'
    BUILDING = 'Building','building'
    USERS = 'Users','users'
    SETTINGS='Settings','settings'
    ARCHIVE = 'Archive','archive'

class PayrollFrequencyEnum(models.TextChoices):
    WEEKLY = 'Weekly','weekly'
    BI_WEEKLY = 'Bi-Weekly','bi-weekly'
    MONTHLY = 'Monthly','monthly'

class ComponentType(models.TextChoices):
    EARNING = 'Earning','earning'
    DEDUCTION = 'Deduction','deduction'

class CalculationType(models.TextChoices):
    FIXED_AMOUNT = 'Fixed Amount', 'fixed amount'
    PERCENTAGE_OF_BASIC = 'Percentage of Basic', 'percentage of basic'

class RequiredType(models.TextChoices):
    YES = 'Yes','yes'
    NO = 'No', 'no'

class JobApplicationType(models.TextChoices):
    EXISTING_LINK= 'Existing Link', 'existing link'
    CUSTOM_LINK = 'Custom Link', 'custom link'

class CandidateStatus(models.TextChoices):
    APPLIED = 'Applied', 'Applied'
    SHORTLISTED = 'Shortlisted', 'Shortlisted'
    INTERVIEW = 'Interview', 'Interview'
    OFFERED = 'Offered', 'Offered'
    HIRED = 'Hired', 'Hired'
    REJECTED = 'Rejected', 'Rejected'

class RecommendationEnum(models.TextChoices):
    STRONG_HIRE='Strong Hire', 'strong hire'
    HIRE='Hire', 'hire'
    MAY_BE='May Be', 'may be'
    REJECT='Reject', 'reject'
    STRONG_REJECT ='Strong Reject', 'strong reject'

class AssessmentEnum(models.TextChoices):
    PASS = 'Pass', 'pass'
    FAIL = 'Fail', 'fail'
    PENDING = 'Pending','pending'

class SymbolPositionEnum(models.TextChoices):
    LEFT = 'before', 'Before Amount  →  $1,234'
    RIGHT = 'after',  'After Amount   →  1,234$'

class EmailProvider(models.TextChoices):
    SMTP = 'smtp', 'SMTP'
    SENDGRID = 'sendgrid', 'SendGrid'
    MAILGUN = 'mailgun', 'Mailgun'
    SES = 'ses', 'Amazon SES'

class SmtpEncryption(models.TextChoices):
    TLS = 'tls', 'TLS'
    SSL = 'ssl', 'SSL'
    NONE = 'none', 'None'

class DocumentTemplateType(models.TextChoices):
    NOC            = 'noc',            'No Objection Certificate'
    EXPERIENCE     = 'experience',     'Experience Certificate'
    JOINING_LETTER = 'joining_letter', 'Joining Letter'

class StorageDriver(models.TextChoices):
    LOCAL = 'local', 'Local'
    S3 = 's3', 'Amazon S3'
    GCS = 'gcs', 'Google Cloud Storage'
    DO_SPACES = 'do_spaces', 'DigitalOcean Spaces'

class CacheDriver(models.TextChoices):
    FILE = 'file', 'File'
    REDIS = 'redis', 'Redis'
    MEMCACHED = 'memcached', 'Memcached'
    DATABASE = 'database', 'Database'

class ButtonStyleEnum(models.TextChoices):
    GRADIENT = 'Gradient','gradient'
    SOLID = 'Solid','solid'
    OUTLINE = 'Outline', 'outline'

class LayoutStyleEnum(models.TextChoices):
    CONTENT = 'Content Left, Image Right'
    IMAGE = 'Image Left, Content Right'
    FULL_WIDTH = 'Full Width'
    CENTERED_CONTENT = 'Centered Content'

class LanguageEnum(models.TextChoices):
    ENGLISH = 'en', 'English'
    HINDI = 'hi', 'Hindi'

class DateFormatEnum(models.TextChoices):
    Y_M_D = 'YYYY-MM-DD', 'YYYY-MM-DD'
    D_M_Y = 'DD-MM-YYYY', 'DD-MM-YYYY'
    M_D_Y = 'MM-DD-YYYY', 'MM-DD-YYYY'

class TimeFormatEnum(models.TextChoices):
    H_I = 'HH:mm', '24 Hours'
    H_I_A = 'hh:mm A', '12 Hours'

class TimeZone(models.TextChoices):
    UTC = 'UTC', 'UTC'
    IST = 'Asia/Kolkata', 'India Standard Time'

class SidebarVarientEnum(models.TextChoices):
    INSET = 'inset', 'Inset'
    DEFAULT = 'default', 'Default'

class SidebarStyleEnum(models.TextChoices):
    PLAIN = 'plain', 'Plain'
    ACCENT = 'accent', 'Accent'

class LayoutDirectionEnum(models.TextChoices):
    LEFT_TO_RIGHT = 'ltr', 'Left to Right'
    RIGHT_TO_LEFT = 'rtl', 'Right to Left'

class ThemeModeEnum(models.TextChoices):
    LIGHT = 'light', 'Light'
    DARK = 'dark', 'Dark'
    SYSTEM = 'system', 'System'

class DecimalSeparatorEnum(models.TextChoices):
    DOT = '.', 'Dot (.)'
    COMMA = ',', 'Comma (,)'

class ThousandsSeparatorEnum(models.TextChoices):
    COMMA = ',', 'Comma (,)'
    DOT = '.', 'Dot (.)'
    SPACE = ' ', 'Space ( )'

class FileTypeEnum(models.TextChoices):
    IMAGE = 'image', 'Image'
    DOCUMENT = 'document', 'Document'
    ALL = 'all', 'All'

class ComplaintStatus(models.TextChoices):
    OPEN = 'open', 'Open'
    IN_PROGRESS = 'in_progress', 'In Progress'
    RESOLVED = 'resolved', 'Resolved'
    CLOSED = 'closed', 'Closed'

class ComplaintType(models.TextChoices):
    GENERAL = 'general', 'General'
    WORKPLACE = 'workplace', 'Workplace'
    PERSONAL = 'personal', 'Personal'

class AssignTrainingStatus(models.TextChoices):
    PENDING = 'pending', 'Pending'
    COMPLETED = 'completed', 'Completed'
    CERTIFIED = 'certified', 'Certified'

class MeetingMinutesType(models.TextChoices):
    FORMAL = 'formal', 'Formal'
    INFORMAL = 'informal', 'Informal'


class AttendanceStatus(models.TextChoices):
    PRESENT = 'present', 'Present'
    ABSENT = 'absent', 'Absent'
    LATE = 'late', 'Late'
    HALF_DAY = 'half_day', 'Half Day'
    ON_LEAVE = 'on_leave', 'On Leave'
    HOLIDAY = 'holiday', 'Holiday'

class LeaveStatus(models.TextChoices):
    PENDING = 'pending', 'Pending'
    APPROVED = 'approved', 'Approved'
    REJECTED = 'rejected', 'Rejected'
    CANCELLED = 'cancelled', 'Cancelled'