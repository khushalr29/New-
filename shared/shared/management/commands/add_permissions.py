from django.core.management.base import BaseCommand
from django.contrib.auth.models import Permission
from django.contrib.contenttypes.models import ContentType
from django.apps import apps
from django.db import IntegrityError

class Command(BaseCommand):
    help = "Exhaustive population of HRMS model permissions into the database"
    
    def handle(self, *args, **kwargs):
        # Format: (name, content_type_str, codename)
        permission_list = [
            # --- Admin & Auth ---
            ("can list log entry", "admin | logentry", "list_logentry"),
            ("can list group", "auth | group", "list_group"),
            ("can list permission", "auth | permission", "list_permission"),

            # --- Core HRMS ---
            ("can list user", "shared | user", "list_user"),
            ("can list company", "shared | company", "list_company"),
            ("can list role", "shared | role", "list_role"),
            ("can list plan", "shared | plan", "list_plan"),
            ("can list subscription", "shared | subscription", "list_subscription"),
            ("can list employee", "shared | employee", "list_employee"),
            ("can list employee designation", "shared | employeedesignation", "list_employeedesignation"),
            ("can list activity log", "shared | useractivitylog", "list_useractivitylog"),
            ("can list calendar schedule", "shared | calenderschedule", "list_calenderschedule"),

            # --- System Settings (Comprehensive) ---
            ("can list system settings", "shared | systemsetting", "list_systemsetting"),
            ("can list brand setting", "shared | brandsetting", "list_brandsetting"),
            ("can list currency setting", "shared | currencysetting", "list_currencysetting"),
            ("can list email setting", "shared | emailsetting", "list_emailsetting"),
            ("can list working days setting", "shared | workingdayssetting", "list_workingdayssetting"),
            ("can list ip restriction settings", "shared | iprestrictionsettings", "list_iprestrictionsettings"),
            ("can list allowed ip", "shared | allowedip", "list_allowedip"),
            ("can list zkteco settings", "shared | zktecosettings", "list_zktecosettings"),
            ("can list document template settings", "shared | documenttemplatesettings", "list_documenttemplatesettings"),
            ("can list storage settings", "shared | storagesettings", "list_storagesettings"),
            ("can list recaptcha settings", "shared | recaptchasettings", "list_recaptchasettings"),
            ("can list chatgpt settings", "shared | chatgptsettings", "list_chatgptsettings"),
            ("can list cookie settings", "shared | cookiesettings", "list_cookiesettings"),
            ("can list custom cookie item", "shared | customcookieitem", "list_customcookieitem"),
            ("can list seo settings", "shared | seosettings", "list_seosettings"),
            ("can list cache settings", "shared | cachesettings", "list_cachesettings"),

            # --- HR Management ---
            ("can list company type", "shared | companytype", "list_companytype"),
            ("can list department", "shared | department", "list_department"),
            ("can list branch", "shared | branch", "list_branch"),
            ("can list designation", "shared | designation", "list_designation"),
            ("can list holiday", "shared | holiday", "list_holiday"),
            ("can list document type", "shared | documenttype", "list_documenttype"),
            ("can list award type", "shared | awardtype", "list_awardtype"),
            ("can list indicator category", "shared | indicatorcategory", "list_indicatorcategory"),
            ("can list indicator", "shared | indicator", "list_indicator"),
            ("can list goal type", "shared | goaltype", "list_goaltype"),
            ("can list review cycle", "shared | reviewcycle", "list_reviewcycle"),
            ("can list resignations", "shared | resignations", "list_resignations"),
            ("can list termination", "shared | termination", "list_termination"),
            ("can list announcement", "shared | announcement", "list_announcement"),
            ("can list assets", "shared | assets", "list_assets"),
            ("can list asset type", "shared | assettype", "list_assettype"),
            ("can list award", "shared | award", "list_award"),
            ("can list complaint", "shared | complaint", "list_complaint"),
            ("can list employee goal", "shared | employeegoal", "list_employeegoal"),
            ("can list employee review", "shared | employeereview", "list_employeereview"),
            ("can list promotion", "shared | promotion", "list_promotion"),
            ("can list transfer", "shared | transfer", "list_transfer"),
            ("can list trip", "shared | trip", "list_trip"),
            ("can list warning", "shared | warning", "list_warning"),
            ("can list training type", "shared | trainingtype", "list_trainingtype"),
            ("can list training program", "shared | trainingprogram", "list_trainingprogram"),
            ("can list training session", "shared | trainingsession", "list_trainingsession"),
            ("can list assign training", "shared | assigntraining", "list_assigntraining"),

            # --- Recruitment ---
            ("can list candidate assessment", "shared | candidateassessment", "list_candidateassessment"),
            ("can list candidate source", "shared | candidatesource", "list_candidatesource"),
            ("can list candidate", "shared | candidate", "list_candidate"),
            ("can list checklist item", "shared | checklistitem", "list_checklistitem"),
            ("can list custom questions", "shared | customquestions", "list_customquestions"),
            ("can list interview type", "shared | interviewtype", "list_interviewtype"),
            ("can list interview round", "shared | interviewround", "list_interviewround"),
            ("can list interview", "shared | interview", "list_interview"),
            ("can list interview feedback", "shared | interviewfeedback", "list_interviewfeedback"),
            ("can list job category", "shared | jobcategory", "list_jobcategory"),
            ("can list job location", "shared | joblocation", "list_joblocation"),
            ("can list job posting", "shared | jobposting", "list_jobposting"),
            ("can list job type", "shared | jobtype", "list_jobtype"),
            ("can list offer", "shared | offer", "list_offer"),
            ("can list offer templates", "shared | offertemplates", "list_offertemplates"),
            ("can list onboarding checklist", "shared | onboardingchecklist", "list_onboardingchecklist"),
            ("can list onboarding", "shared | onboarding", "list_onboarding"),

            # --- Attendance & Leave ---
            ("can list shift", "shared | shift", "list_shift"),
            ("can list leave type", "shared | leavetype", "list_leavetype"),
            ("can list leave application", "shared | leaveapplication", "list_leaveapplication"),
            ("can list leave balance", "shared | leavebalance", "list_leavebalance"),
            ("can list leave policy", "shared | leavepolicy", "list_leavepolicy"),
            ("can list time entries", "shared | timeentries", "list_timeentries"),

            # --- Payroll ---
            ("can list payroll run", "shared | payrollrun", "list_payrollrun"),
            ("can list salary component", "shared | salarycomponent", "list_salarycomponent"),

            # --- Meetings ---
            ("can list action items", "shared | actionitem", "list_actionitem"),
            ("can list meeting minutes", "shared | meetingminutes", "list_meetingminutes"),
            ("can list meeting room", "shared | meetingroom", "list_meetingroom"),
            ("can list meeting attendee", "shared | meetingattendee", "list_meetingattendee"),
            ("can list meeting", "shared | meeting", "list_meeting"),
            ("can list meeting type", "shared | meetingtype", "list_meetingtype"),

            # --- Documents & Contracts ---
            ("can list acknowledgement", "shared | acknowledgement", "list_acknowledgement"),
            ("can list document template", "shared | documenttemplate", "list_documenttemplate"),
            ("can list hr document", "shared | hrdocument", "list_hrdocument"),
            ("can list document categories", "shared | documentcategories", "list_documentcategories"),
            ("can list contract template", "shared | contracttemplate", "list_contracttemplate"),
            ("can list contract type", "shared | contracttype", "list_contracttype"),
            ("can list employee contract", "shared | employeecontract", "list_employeecontract"),

            # --- Import/Export ---
            ("can import employee as csv", "shared | employee", "import_employee_csv"),
            ("can export employee", "shared | employee", "export_employee"),
        ]

        for name, content_type_str, codename in permission_list:
            app_label, model_name = content_type_str.split(" | ")
            try:
                model = apps.get_model(app_label, model_name)
                content_type = ContentType.objects.get_for_model(model)
                
                permission, created = Permission.objects.get_or_create(
                    name=name,
                    content_type=content_type,
                    codename=codename
                )
                
                status_text = "Created" if created else "Updated"
                self.stdout.write(self.style.SUCCESS(f"{status_text} permission: {codename}"))
                
            except LookupError:
                self.stdout.write(self.style.ERROR(f"Couldn't find model for {content_type_str}"))
            except Exception as e:
                self.stdout.write(self.style.ERROR(f"Error for {codename}: {str(e)}"))

        self.stdout.write(self.style.SUCCESS("Exhaustive HRMS Permissions populated successfully!"))