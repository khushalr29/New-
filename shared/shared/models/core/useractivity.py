from .user import User
from django.db import models
from .company import Company
from django.utils import timezone

class UserActivityLog(models.Model):
    LOGIN = 'login'
    LOGOUT = 'logout'
    CREATE = 'create'
    UPDATE = 'update'
    DELETE = 'delete'
    VIEW = 'view'
    LIST = 'list'
    EXPORT = 'export'
    IMPORT = 'import'
    RENEW = 'renew'
    UPGRADE = 'upgrade'
    RESCHEDULE = 'reschedule'
    CANCEL = 'cancel'
    CHANGE_STATUS = 'change_status'
    IMPERSONATION_LOGIN_AS = 'impersonation_login_as'

    ACTION_CHOICES = [
        (LOGIN, 'Login'),
        (LOGOUT, 'Logout'),
        (CREATE, 'Create'),
        (UPDATE, 'Update'),
        (DELETE, 'Delete'),
        (VIEW, 'View'),
        (LIST, 'List'),
        (EXPORT, 'Export'),
        (IMPORT, 'Import'),
        (RENEW, 'Renew'),
        (UPGRADE, 'Upgrade'),
        (RESCHEDULE, 'Reschedule'),
        (CANCEL, 'Cancel'),
        (CHANGE_STATUS, 'Change Status'),
        (IMPERSONATION_LOGIN_AS, 'Impersonation login as'),
    ]

    SUCCESS = 'success'
    FAILED = 'failed'

    STATUS_CHOICES = [
        (SUCCESS, 'Success'),
        (FAILED, 'Failed'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    action = models.CharField(max_length=30, choices=ACTION_CHOICES)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default=SUCCESS)
    resource = models.CharField(max_length=100, blank=True, null=True)
    resource_id = models.IntegerField(blank=True, null=True)
    timestamp = models.DateTimeField(default=timezone.now)
    company = models.ForeignKey(Company, on_delete=models.CASCADE, blank=True, null=True)
    client_ip = models.GenericIPAddressField(blank=True, null=True)
    tracing_id = models.UUIDField(blank=True, null=True)
    request_method = models.CharField(max_length=10, blank=True, null=True)
    endpoint = models.TextField(blank=True, null=True)
    request_data = models.JSONField(blank=True, null=True)
    response_data = models.JSONField(blank=True, null=True)
    execution_time = models.FloatField(blank=True, null=True)
    user_agent = models.TextField(blank=True, null=True)
    system_info = models.JSONField(blank=True, null=True)

    def __str__(self):
        return f"{self.user.username} {self.action} ({self.status}) {self.resource} {self.resource_id} at {self.timestamp}"