from enum import Enum

class UploadCategory(Enum):
    PROFILE_IMAGES = {
        "LOCATION": "profile/images",
        "EXTENSIONS": ["png", "jpeg", "jpg"],
        "ACCEPT": ["image/png", "image/jpeg", "image/jpg"],
        "MAX_FILES": 1,
        "MAX_SIZE": 10485760,
    }
    EMPLOYEE_DOCUMENTS = {
        "LOCATION": "employee/documents",
        "EXTENSIONS": ["pdf", "png", "jpeg", "jpg"],
        "ACCEPT": ["application/pdf", "image/png", "image/jpeg", "image/jpg"],
        "MAX_FILES": 5,
        "MAX_SIZE": 10485760,
    }
    CANDIDATE_RESUMES = {
        "LOCATION": "recruitment/resumes",
        "EXTENSIONS": ["pdf", "doc", "docx"],
        "ACCEPT": ["application/pdf", "application/msword", "application/vnd.openxmlformats-officedocument.wordprocessingml.document"],
        "MAX_FILES": 1,
        "MAX_SIZE": 10485760,
    }
    OFFER_LETTERS = {
        "LOCATION": "recruitment/offers",
        "EXTENSIONS": ["pdf"],
        "ACCEPT": ["application/pdf"],
        "MAX_FILES": 1,
        "MAX_SIZE": 10485760,
    }
    ASSET_IMAGES = {
        "LOCATION": "assets/images",
        "EXTENSIONS": ["png", "jpeg", "jpg"],
        "ACCEPT": ["image/png", "image/jpeg", "image/jpg"],
        "MAX_FILES": 3,
        "MAX_SIZE": 10485760,
    }
    COMPANY_LOGO = {
        "LOCATION": "company/logo",
        "EXTENSIONS": ["svg", "png", "jpeg", "jpg"],
        "ACCEPT": ["image/svg+xml", "image/png", "image/jpeg", "image/jpg"],
        "MAX_FILES": 1,
        "MAX_SIZE": 5242880,
    }
    LEAVE_ATTACHMENTS = {
        "LOCATION": "leave/attachments",
        "EXTENSIONS": ["pdf", "png", "jpeg", "jpg"],
        "ACCEPT": ["application/pdf", "image/png", "image/jpeg", "image/jpg"],
        "MAX_FILES": 1,
        "MAX_SIZE": 10485760,
    }

class SubscriptionModels(Enum):
    COMPANY = "company"
    PLAN = "plan"
    SUBSCRIPTION = "subscription" 

class BillingModels(Enum):
    PAYROLLRUN = "payrollrun"
    SALARYCOMPONENT = "salarycomponent"
    PAYMENTENTRY = "paymententry"

class CoreModels(Enum):
    EMPLOYEE = "employee"
    USER = "user"
    DEPARTMENT = "department"
    BRANCH = "branch"
    DESIGNATION = "designation"
    ROLE = "role"

class PrintAppModelS(Enum):
    DOCUMENTTEMPLATE = "documenttemplate"
    OFFERTEMPLATE = "offertemplate"
    CONTRACTTEMPLATE = "contracttemplate"
    NOTIFICATIONTEMPLATE = "notificationtemplate"

class DependencyPermissions(Enum):
    # --- Employee Management ---
    ADD_EMPLOYEE = {'DEPENDENCIES': ['view_employee', 'list_employee', 'view_department', 'view_designation', 'view_branch']}
    CHANGE_EMPLOYEE = {'DEPENDENCIES': ['view_employee', 'list_employee']}
    DELETE_EMPLOYEE = {'DEPENDENCIES': ['view_employee', 'list_employee']}
    LIST_EMPLOYEE = {'DEPENDENCIES': ['view_company']}

    # --- Recruitment ---
    ADD_JOBPOSTING = {'DEPENDENCIES': ['view_jobposting', 'list_jobposting', 'view_department', 'view_branch']}
    ADD_CANDIDATE = {'DEPENDENCIES': ['view_candidate', 'list_candidate', 'view_jobposting']}
    ADD_INTERVIEW = {'DEPENDENCIES': ['view_interview', 'list_interview', 'view_candidate', 'view_employee']}
    ADD_OFFER = {'DEPENDENCIES': ['view_offer', 'list_offer', 'view_candidate']}

    # --- Leave & Attendance ---
    ADD_LEAVEAPPLICATION = {'DEPENDENCIES': ['view_leaveapplication', 'list_leaveapplication', 'view_employee', 'view_leavetype']}
    ADD_TIMEENTRIES = {'DEPENDENCIES': ['view_timeentries', 'list_timeentries', 'view_employee']}

    # --- Payroll ---
    ADD_PAYROLLRUN = {'DEPENDENCIES': ['view_payrollrun', 'list_payrollrun', 'view_employee', 'view_salarycomponent']}

    # --- HR Ops ---
    ADD_ANNOUNCEMENT = {'DEPENDENCIES': ['view_announcement', 'list_announcement', 'view_branch', 'view_department']}
    ADD_PROMOTION = {'DEPENDENCIES': ['view_promotion', 'list_promotion', 'view_employee', 'view_designation']}
    ADD_TRANSFER = {'DEPENDENCIES': ['view_transfer', 'list_transfer', 'view_employee', 'view_branch', 'view_department']}
    
    # --- Meetings ---
    ADD_MEETING = {'DEPENDENCIES': ['view_meeting', 'list_meeting', 'view_meetingroom', 'view_employee']}

    # --- Core Admin ---
    ADD_USER = {'DEPENDENCIES': ['view_user', 'list_user', 'view_role']}
    ADD_DEPARTMENT = {'DEPENDENCIES': ['view_department', 'list_department']}
    ADD_DESIGNATION = {'DEPENDENCIES': ['view_designation', 'list_designation', 'view_department']}
    ADD_ROLE = {'DEPENDENCIES': ['view_role', 'list_role']}
