class ResponseMessages:
    VALID_WEEKDAYS = ["monday", "tuesday", "wednesday", "thursday", "friday", "saturday", "sunday"]
    SUCCESS = "Success"
    WARNING = "Warning"
    BAD_REQUEST = "Bad Request"
    UNAUTHORIZED = "Authentication credentials required."
    LOGIN_SUCCESS = "Login successful"
    LOGOUT_SUCCESS = "Logout successful"
    NOT_REGISTERED_USER = "User not registered"
    FORBIDDEN = "Insufficient permissions to access this resource."
    NOT_FOUND = "Not Found"
    TOO_MANY_REQUESTS = "Too Many Requests"
    SERVER_ERROR = "Server Error"
    CREATE_FAILED = "creation failed."
    DELETE_FAILED = "deletion failed."
    UPDATE_FAILED = "update failed."
    VALIDATION_ERROR = "Validation error."
    UNEXPECTED_ERROR = "Unexpected error occurred."
    NO_MATCHING_DATA = "No matching data found."
    PASSWORD_MISMATCH = "Passwords don't match"
    INVALID_TOKEN = "Invalid or expired token"
    DOCTOR_NOT_FOUND = "No doctor found for this department."
    DATA_FETCH_SUCCESS = "Data fetched successfully."
    DATA_FETCH_FAILED = "Error fetching data: {error}"
    INVALID_TIME_FORMAT = "Invalid time format in slot '{slot}'. Use 'HH:MM-HH:MM'."
    START_TIME_AFTER_END = "Start time must be before end time in slot '{slot}'."
    INVALID_WEEKDAY = "Invalid weekday: {day}."
    EMPTY_TIME_SLOTS = "{day} must have at least one time slot."
    OVERLAPPING_TIME_SLOTS = "Overlapping time slots on {day}: {slot1} and {slot2}"
    EMAIL_ALREADY_IN_USE = "Email already in use. Please use a different one."
    PHONE_ALREADY_IN_USE = "Phone number already in use."
    PASSWORD_UPDATED = "Password updated"
    PASSWORD_EMAIL_SENT = "Password reset email sent successfully."
    USER_CREATION_EMAIL_NOTICE = "User created. Please check email to set password."
    STAFF_NOT_FOUND = "Staff not found"
    PERMISSION_NOT_FOUND = "Permission with ID {id} not found."
    NO_PERMISSIONS_PROVIDED = "No permission IDs provided for assignment or removal."
    PERMISSION_ASSIGN_SUCCESS = "Permissions updated successfully."
    USER_PERMISSIONS_FETCH_SUCCESS = "User permissions fetched successfully."
    USER_NOT_FOUND = "User not found."
    NO_IDS_PROVIDED = "No IDs provided for deletion."
    GROUP_CONNECTED = "Group '{group_name}' is connected to a user and cannot be deleted."
    ADMIN_GROUP_CANNOT_BE_DELETED = "Admin group cannot be deleted."
    NO_PERMISSIONS_OR_NAME_PROVIDED = "No permissions or group name provided for assignment, removal, or update."
    GROUPS_REQUIRED = "'groups' required in request body."
    GROUP_ID_AND_ACTION_REQUIRED = "Group IDs and action required for each group."
    INVALID_ACTION = "Invalid action. Use 'enable' or 'disable'."
    GROUP_UPDATE_SUCCESS = "User '{user_id}' updated with groups {group_ids}."
    GROUP_NOT_FOUND = "Group not found."
    AGE_MISMATCH = "Age doesn't match date of birth. Calculated age is {calculated_age}."
    INVALID_SLOTS = "Invalid slot format: {slot}. Use 'HH:MM-HH:MM'."
    INVALID_NEXT_VISIT_DATE = "Invalid next visit date. Check 'next_visit_in_days'."
    INVALID_DATE_FORMAT = "Invalid date format. Use YYYY-MM-DD."
    NO_AVAILABILITY = "No availability for this doctor on {date}."
    INVALID_SLOT_FORMAT = "Invalid slot format: {slot}. Use 'HH:MM-HH:MM'. Details: {error_details}"
    SUCCESS_FETCH = "Appointment slots data fetched successfully."
    GENERAL_ERROR = "Unexpected error: {error_message}"
    NO_PERMISSION = "No permission to view appointment slots."
    PHONE_REQUIRED = "Phone number required"
    MISMATCH_PROFILE = "No doctor profile associated with this user."
    INVALID_CREDENTIALS = "Invalid credentials. Check email and password."
    USER_ACCOUNT_DISABLED = "User account disabled."
    ACCESS_GRANTED = "Access granted."
    SUBSCRIPTION_UPGRADED = "Subscription upgraded successfully"
    SUBSCRIPTION_RENEWED = "Subscription renewed successfully."
    PAYMENT_INITIATED = "Payment link sent successfully."
    PAYMENT_SUCCESS = "Payment successful."
    PAYMENT_FAILED = "Payment failed, subscription marked as failed."
    PAYMENT_GATEWAY_INVALID_RESPONSE = "Invalid response from payment gateway."
    PAYMENT_TOKEN_MISSING = "Payment token missing or malformed."
    SUBSCRIPTION_NOT_FOUND = "Subscription not found for this transaction."
    INVALID_JSON_RESPONSE = "Invalid JSON response from payment gateway."
    PAYMENT_GATEWAY_ERROR = "Payment gateway error occurred."
    MISSING_TXNID_OR_STATUS = "Missing transaction ID or status."
    PAYMENT_INITIATION_FAILED = "Unable to initiate payment"
    AUTH_HEADER_MISSING_OR_INVALID = "Authorization header missing or invalid"
    TOKEN_EXPIRED = "Token expired"
    INVALID_TOKEN = "Invalid token"
    INVALID_TOKEN_SUBJECT = "Invalid token subject"
    USER_NOT_FOUND = "User not found"
    COMPANY_NOT_FOUND = "Company not found"
    TOKEN_MISSING_IAT = "Token missing 'iat' claim"
    USER_TOKEN_ISSUED_AT_MISSING = "User token issue timestamp missing"
    SESSION_EXPIRED = "Session expired"
    COMPANY_SUBSCRIPTION_EXPIRED_CONTACT_ADMIN = "Company subscription expired. Contact company to renew."
    COMPANY_SUBSCRIPTION_EXPIRED = "Company subscription expired"
    ACCOUNT_SUSPENDED = "Account suspended"
    PAYMENT_MODE_ERROR = "Only online payment allowed for your access level."
    ID_REQUIRED = "IDs required"
    SUBSCRIBED_PLAN_ERROR = "Company already subscribed to this plan."
    INVALID_DOCTOR_SCHEDULE = "Invalid doctor schedule"
    SUBSCRIPTION_USER_ERROR = "Not authorized to renew subscription for this company."
    RENEW_SUBSCRIPTION_PLAN_ERROR = "Company has different subscribed plan."
    MAX_USER_ERROR = "Company reached user limit ({max_users}) for selected plan."
    REQUEST_NOT_ASSIGNED = "Only assigned requests can be completed."
    REQUEST_COMPLETED_SUCCESS = "Request marked as completed successfully"
    NOT_ACTIVE_PLAN = "Company has no active plan to renew."
    IMPERSONATION_LOGIN_USER_ERROR = "Only superusers or super admins can perform impersonation login."
    TARGET_ID_ERROR = "Target company ID required."
    TARGET_USER_ERROR = "Target user not found."
    TARGET_SUPERUSER_ERROR = "Cannot impersonate a superuser."
    IMPERSONATION_NOT_ALLOWED = "Not authorized to perform this action."
    INVALID_EXPIRY_DATE = "Expiry date must be after or equal to manufacturing date."
    DELETE_ERROR = "Cannot delete - data is connected."
    EXTENSION_ERROR = "Extensions must be a list of strings."
    INVALID_GLOBAL_SEARCH_TYPE = "Invalid search type. Must be: Patient, Doctor, or Staff."
    SUBDOMAIN_ERROR = "Invalid company domain for user."
    GST_NUMBER_EXISTS = "GST number already exists."
    SERVICE_NOT_AVAILABLE = "Service not available in your Company."
    REQUEST_ALREADY_ASSIGNED = "Request already assigned. Complete before re-assigning."
    UPDATE_NOT_ALLOWED = "Ambulance request already assigned and cannot be updated."
    REQUEST_ASSIGNED_SUCCESS = "Request assigned successfully."
    NAME_TOO_SHORT = "Name must be at least 3 characters long."
    NAME_START_END_DOT = "Name cannot start or end with a dot (.)"
    NAME_INVALID_CHARS = "Name must start with a letter and include only letters, numbers, spaces, dots, underscores, or hyphens."
    DOMAIN_INVALID_FORMAT = "Domain must be in format https://<subdomain>.hrms.in"
    GST_INVALID = "Invalid GST number format."
    ADDRESS_EMPTY = "{field_name} cannot be empty."
    ADDRESS_TOO_SHORT = "{field_name} must be at least 3 characters long."
    ADDRESS_ALPHA_REQUIRED = "{field_name} must contain at least one alphabet character."
    ADDRESS_SPECIAL_ONLY = "{field_name} cannot be only special characters or numbers."
    ADDRESS_INVALID_CHARACTERS = "{field_name} contains invalid characters. Allowed: {allowed_chars}"
    ADDRESS_EMOJI_NOT_ALLOWED = "{field_name} cannot contain emojis."
    ADDRESS_DISALLOWED_SPECIALS = "{field_name} contains disallowed special characters."
    ADDRESS_START_END_AT = "{field_name} cannot start or end with '@'."
    ROOM_INVALID = "Room number must be a valid integer without letters or special characters."
    STAFF_AS_USER_ERROR = "User not associated with any staff."
    CHAR_FIELD_EMPTY = "{field_name} cannot be empty."
    CHAR_FIELD_TOO_SHORT = "{field_name} must be at least {min_length} characters."
    CHAR_FIELD_TOO_LONG = "{field_name} must not exceed {max_length} characters."
    CHAR_FIELD_INVALID_CHARS = "{field_name} contains invalid characters. Only letters, numbers, space, dot, underscore and hyphen allowed."
    INTEGER_REQUIRED = "{field_name} must be an integer."
    INTEGER_TOO_SMALL = "{field_name} must be at least {min_value}."
    INTEGER_TOO_LARGE = "{field_name} must not exceed {max_value}."
    ADDRESS_ALPHA_REQUIRED = "{field_name} should only contain alphabetic characters."
    NAME_TOO_SHORT = "{field_name} must be at least 3 characters."
    NAME_START_END_DOT = "{field_name} cannot start or end with a dot (.)"
    NAME_INVALID_CHARS = "{field_name} contains invalid characters. Only letters, numbers, space, dot, underscore and hyphen allowed."
    DOMAIN_INVALID_FORMAT = "Domain must be in format 'https://<subdomain>.okcare.in'."
    GST_INVALID = "Invalid GST number format."
    ADDRESS_EMPTY = "{field_name} cannot be empty."
    ADDRESS_SPECIAL_ONLY = "{field_name} cannot contain only special characters."
    ADDRESS_START_END_AT = "{field_name} cannot start or end with '@'."
    ADDRESS_INVALID_CHARACTERS = "{field_name} contains invalid characters. Only {allowed_chars} are allowed."
    ADDRESS_EMOJI_NOT_ALLOWED = "{field_name} should not contain emojis."
    ADDRESS_DISALLOWED_SPECIALS = "{field_name} contains disallowed special characters like < > ^ $ * # { } [ ] \\ ` ~ |"
    ROOM_INVALID = "{field_name} must contain only letters, numbers, hyphens, and spaces."
    PHONE_TYPE_INVALID = "{} must be a string or integer."
    PHONE_SHOULD_NOT_INCLUDE_PLUS = "{} should not include '+'."
    PHONE_FORMAT_INVALID = "{field_name} is invalid."
    PHONE_PARSE_ERROR = "Invalid phone number format: {error}"
    PHONE_NOT_POSSIBLE = "{} is not a valid phone number length."
    PHONE_INVALID_FOR_REGION = "{} does not match regional rules."
    INVALID_MPIN = "{field_name} must be exactly 6 digits."
    MPIN_LENGTH_ERROR = "mPIN must be exactly 6 digits."
    MPIN_UPDATED = "mPIN set successfully."
    INVALID_FORMAT = "{field_name} must be in format 0-1-0-1, where each value is 0 or 1."
    INVALID_FIELD = "{field_name} is invalid. Provide valid dose format."
    INVALID_DECIMAL = "{field_name} should be a positive decimal number."
    OTP_SENT = "OTP sent to your registered email."
    INVALID_OTP = "Invalid or expired OTP."
    MPIN_UPDATED = "mPIN set successfully."
    USER_HAS_NO_COMPANY = "User has no company assigned."
    ROOM_ALREADY_BOOKED = "Selected OT room already booked for this time."
    ROOM_ALREADY_EXISTS = "Room with this number already exists."
    INVALID_ACTION = "Invalid action provided. Must be 'enable' or 'disable'."
    ROOM_ALREADY_ENABLED = "Room already enabled."
    ROOM_ALREADY_DISABLED = "Room already disabled."
    ROOM_ENABLED_SUCCESS = "Room enabled successfully."
    ROOM_DISABLED_SUCCESS = "Room disabled successfully."
    NO_MATCHING_ROOMS = "No matching rooms found for filter"
    MPIN_NOT_SET = "mPIN not set for this user."
    INVALID_MPIN = "mPIN must be a number."
    MPIN_INPUT_DOES_NOT_MATCH_SET = "Entered mPIN doesn't match saved mPIN."
    REMINDER_SENT = "Reminder sent for Appointment {id}, SID: {sid}"
    TWILIO_NOT_FOUND = "No enabled Twilio account found for hospital ID {id}"
    REMINDER_SEND_ERROR = "Error sending reminder for Appointment {id}: {error}"
    REMINDER_SCHEDULED = "Scheduled reminders for {count} upcoming appointments."
    REMINDER_SCHEDULE_FAIL = "Failed to schedule reminder for Appointment ID {id}: {error}"
    AGE_VALIDATION = 'Age must be positive integer'
    REMINDER_SCHEDULING_FAILED = "Reminder scheduling failed → ID: {id} | Error: {error}"
    SCHEDULE_REMINDER_SUMMARY = "Summary → Total: {total}, Scheduled: {scheduled}"
    GST_INVALID = "Invalid GST number format."
    GST_MUST_BE_STRING = "GST number must be a valid string or number."
    DATE_IN_FUTURE = "Date of death cannot be in the future."
    MPIN_VERIFIED = "mPIN verified successfully."
    PASSWORD_VERIFIED = "Password verified."
    AGE_TOO_YOUNG = "Donor age must be at least 18 years."
    AGE_TOO_OLD = "Donor age must not exceed 65 years."
    REQUIRED_FIELD = "{} is required."
    STAFF_CREATED = "Staff created successfully."
    USER_ALREADY_EXISTS = "User already exists with name: {name}. Staff creation rolled back."
    STAFF_AND_USER_CREATED = "Staff and User"
    STAFF_CREATION_FAILED = "Staff creation failed."
    USER_CREATION_FAILED = "User creation failed. Staff creation rolled back."
    MISSING_EMAIL_PHONE = "Email and phone number required to create user from staff."
    INVALID_STAFF_ID = "Staff ID required."
    USER_ALREADY_LINKED = "User already linked to this staff: {name}"
    SOURCE_ADMISSION_OTHER_REQUIRED = "Please specify source of admission if 'Other' is selected."
    CASE_INSENSITIVE_EXISTS = "{} already exists."
    CASE_INSENSITIVE_UNIQUE_TOGETHER = "{} already exists."
    CASE_INSENSITIVE_EMAIL_EXISTS = "{} already exists with this email."
    CASE_INSENSITIVE_NUMBER_EXISTS = "{} already exists with this number."
    CASE_INSENSITIVE_DOMAIN_EXISTS = "{} already exists. Please choose another subdomain."
    CASE_INSENSITIVE_NAME_EXISTS = "{} already exists with this name."
    NOT_ASSOCIATED_USER = "Doctor not associated with any user."
    IPD_ADMISSION_BY_REQUEST = "IPD Admission created from IPD Request"
    NOT_IN_PENDING = "Only pending admissions can be updated to admitted"
    NAME_START_LETTER = "Name must start with an alphabet character."
    ONLY_THESE_ARE_ALLOWED = "Only 'reason_for_admission' and 'doctor_name' can be updated."
    DONE_IPD_REQUEST = "IPD Request"
    ALREADY_PRESENT = "Admission already exists for this patient."
    NOT_TO_DELETED = "Admission present for this request and cannot be deleted."
    NOT_VALID_APPOINTMENT = "Doctor not provided and no valid appointment found."
    BOOKING_CONFIRMED = 'Demo booking request submitted successfully'
    FAILED_BOOKING_PROCESS = 'Failed to process demo booking request'
    APPOINTMENT_BOOKED = 'Booked successfully'
    NO_EMAILS_PROVIDED = "Emails not provided."
    EMAIL_ERROR = "Email not sent."
    ID_REQUIRED_FOR_STATUS = "ID required for status change."
    COLLECTION_DATE_ERROR = "Collection date cannot be in the future."
    REQUIRED_DATE_ERROR = "Required by date cannot be more than 30 days in the future."
    REQUESTED_DATE_ERROR = "Required by date must be in the future."
    CAPTCHA_REQUIRED = "CAPTCHA required"
    DOB_ERROR = "DOB should be in past"
    ALREADY_PRESENT = "Already present"
    ID_RQUIRED = "Id Required"
    EXPIARY_DATE_ERROR = "Expiary date error"
    INVALID_EMAIL = "Invalid email format"
    INVALID_DEPARTMENT_ID = " Invalid Department ID."
    FILE_SIZE_EXCEEDED = "File size exceeds maximum limit of {size}MB. Please upload a smaller file."
    CSV_ERROR = "CSV file not readable. Ensure it's in UTF-8 or Latin-1 encoding."
    INVALID_EXCEL_FORMAT = "Invalid Excel file. Ensure it's a valid .xlsx file. Error: {error}"
    FILE_TOO_LARGE_ROWS = "File contains {rows} rows, exceeding the {max_rows} row limit. Please split and import in batches."
    UPLOADING_VALIDATION_ERROR = "No valid data rows found in the uploaded file."
    FILE_TOO_LARGE_TO_PROCESS = "File too large. Reduce size or split into smaller files."
    INSUFFICIENT_MEMORY_TO_VALIDATE = "Not enough memory to process file. Please reduce its size."
    VALIDATION_ERRORS_FOUND = "Found {error_count} validation error(s). Please fix and try again."
    INSUFFICIENT_MEMORY_TO_IMPORT = "Insufficient memory to import file. Reduce file size or contact support."
    IMPORT_COMPLETED_WITH_ERRORS = "Import completed with {error_count} error(s)."
    IMPORT_SUCCESSFUL = "Successfully imported {record_count} {model_name} record(s)."
    

    @staticmethod
    def success_fetch(data):
        return {
            "message": ResponseMessages.SUCCESS_FETCH,
            "data": data
        }

    @staticmethod
    def general_error(error_message: str):
        return ResponseMessages.GENERAL_ERROR.format(error_message=error_message)
    
    @staticmethod
    def invalid_date_format():
        return ResponseMessages.INVALID_DATE_FORMAT

    @staticmethod
    def no_permission():
        return ResponseMessages.NO_PERMISSION

    @staticmethod
    def create_success_message(name: str):
        return f"{name} added successfully."

    @staticmethod
    def update_success_message(name: str):
        return f"{name} updated successfully."

    @staticmethod
    def delete_success_message(count: int):
        return f"{count} deleted successfully."
    
    @staticmethod
    def not_found(name: str):
        return f"{name} not found"
    
    @staticmethod
    def partial_delete_message(connected_staffs: any):
        return "Some were deleted, but some could not be deleted due to existing connections."

    @staticmethod
    def none_deleted_message(connected_staffs: any):
        return "No were deleted."

    @staticmethod
    def validation_error_message():
        return "Validation error."

    @staticmethod
    def invalid_time_format(slot):
        return ResponseMessages.INVALID_TIME_FORMAT.format(slot=slot)
    
    @staticmethod
    def normalize_days(value):
        return {day.lower(): timeslots for day, timeslots in value.items()}

    @staticmethod
    def start_time_after_end(slot):
        return ResponseMessages.START_TIME_AFTER_END.format(slot=slot)

    @staticmethod
    def invalid_weekday(day):
        return ResponseMessages.INVALID_WEEKDAY.format(day=day)

    @staticmethod
    def empty_time_slots(day):
        return ResponseMessages.EMPTY_TIME_SLOTS.format(day=day)

    @staticmethod
    def overlapping_time_slots(day, slot1, slot2):
        return ResponseMessages.OVERLAPPING_TIME_SLOTS.format(day=day, slot1=slot1, slot2=slot2)
    
    @staticmethod
    def field_required(field):
        return f"{field} field is required"
    
    
    @staticmethod
    def age_mismatch(calculated_age):
        return ResponseMessages.AGE_MISMATCH.format(calculated_age=calculated_age)

    @staticmethod
    def invalid_appointment_id(appointment_id):
        return f'Appointment ID "{appointment_id}" already exists. Please try again.'

    @staticmethod
    def invalid_time_format(time):
        return ResponseMessages.INVALID_TIME_FORMAT.format(time)
    
    @staticmethod
    def invalid_slots(slots):
        return ResponseMessages.INVALID_SLOTS.format(slots)

    @staticmethod
    def model_not_found(model_name: str):
        return f'Model "{model_name}" not found.'

    @staticmethod
    def unsupported_format(file_format: str):
        return f'Unsupported format "{file_format}".'

    @staticmethod
    def file_parsing_failed(error: str):
        return f'File parsing failed: {error}'

    @staticmethod
    def missing_mandatory_fields(fields: list[str]):
        return f'Missing mandatory fields: {", ".join(fields)}'

    @staticmethod
    def import_success(model_name: str):
        return f'Data imported into "{model_name}" successfully'

    @staticmethod
    def import_partial_failure():
        return "Some rows failed to import."

    @staticmethod
    def model_name_required():
        return "Model name must be provided."

    @staticmethod
    def file_missing():
        return "Upload file is missing."

    @staticmethod
    def export_format_invalid(file_format: str):
        return f"Export failed. Invalid file format '{file_format}'."
    
    @staticmethod
    def export_success(model_name: str):
        return f'Exported data for "{model_name}" successfully.'
    
    @staticmethod
    def invalid_appointment_id(appointment_id):
        return f'Appointment ID "{appointment_id}" already exists. Please try again.'
    
    @staticmethod
    def user_not_created(full_name):
        return f'user {full_name} already in onborded'
    
    @staticmethod
    def invalid_credentials():
        return ResponseMessages.INVALID_CREDENTIALS

    @staticmethod
    def user_account_disabled():
        return ResponseMessages.USER_ACCOUNT_DISABLED

    @staticmethod
    def unauthorized():
        return ResponseMessages.UNAUTHORIZED
    
    @staticmethod
    def forbidden():
        return ResponseMessages.FORBIDDEN
    
    @staticmethod
    def access_granted():
        return ResponseMessages.ACCESS_GRANTED
    
    @staticmethod
    def max_user(max_users):
        return ResponseMessages.MAX_USER_ERROR.format(max_users)
    
    @staticmethod
    def protected_error(model_name):
        return (
            f"Cannot delete {model_name}: it is referenced by other records."
        )
    
    @staticmethod
    def already_exists(name: str):
        return f"{name} already exists."