from django.db import models
from .company import Company
from django.utils.timezone import now
from .role import Role
from django.contrib.auth.models import BaseUserManager,AbstractUser,Permission
from .enums import Gender,UserStatus

class UserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError('User must have an email address')

        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)

        user = self.model(
            email=self.normalize_email(email),
            **extra_fields
        )
        
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('account_type', 'super_admin')

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self.create_user(email, password, **extra_fields)

class User(AbstractUser):
    image = models.TextField(blank=True, null=True)
    email = models.EmailField(verbose_name='Email', max_length=255, unique=True)
    full_name = models.CharField(max_length=80)
    country_number_code = models.PositiveIntegerField(default=91)
    phone_number = models.CharField(max_length=15)
    gender = models.CharField(max_length=50,choices=Gender.choices)
    is_enabled = models.BooleanField(default=True)
    roles = models.ManyToManyField(Role,related_name='custom_user_set',blank=True,)
    status = models.CharField(max_length=20,choices=UserStatus.choices,default=UserStatus.ACTIVE)
    user_permissions = models.ManyToManyField(Permission,related_name='custom_user_permissions_set',blank=True,)
    mpin = models.IntegerField(null=True, blank= True)
    is_email_verified = models.BooleanField(default=False)
    SUPER_ADMIN = 'super_admin'
    SUB_ADMIN = 'sub_admin'
    COMPANY_SUPER_ADMIN = 'company_super_admin'
    COMPANY_SUB_ADMIN = 'company_sub_admin'
    account_type = models.CharField(max_length=32, default='sub_admin')
    auth_token_issued_at = models.DateTimeField(null=True, blank=True, default=now)
    company = models.ForeignKey(Company, on_delete=models.CASCADE, null=True, blank=True)
    username = None

    first_name = None
    last_name = None
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    deleted_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        db_table = 'user'
        unique_together = ('email', 'company')
        ordering = ['-created_at']
        verbose_name = 'User'
        verbose_name_plural = 'Users'

    def __str__(self):
        return f"{self.full_name} ({self.email})"

    def clean(self):
        super().clean()
        if self.company and not self.id:
            user_count = User.objects.filter(company=self.company).count()
            if user_count >= self.company.no_of_users:
                 from django.core.exceptions import ValidationError
                 raise ValidationError("Company reached user limit for the selected plan.")

    def save(self, *args, **kwargs):
        self.clean()
        super().save(*args, **kwargs)

    def has_permission(self, codename):
        if self.user_permissions.filter(codename=codename).exists():
            return True
        
        for group in self.roles.all():
            if group.permissions.filter(codename=codename).exists():
                return True
        return False
    
    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['full_name', 'phone_number', 'gender', 'account_type']

    def has_perm(self, obj=None):
        return self.is_superuser

    def has_module_perms(self, app_label):
        return True

    @property
    def is_mpin_set(self):
        """Returns True if user has configured their mobile pin."""
        return self.mpin is not None

    @property
    def is_staff(self):
        """True if user is either Global or Company Super Admin."""
        return self.account_type in [self.SUPER_ADMIN, self.COMPANY_SUPER_ADMIN]
    
    @is_staff.setter
    def is_staff(self, value):
        self._is_staff = value

    @property
    def is_super_admin(self):
        return self.account_type == self.SUPER_ADMIN

    @property
    def is_sub_admin(self):
        return self.account_type == self.SUB_ADMIN

    @property
    def is_company_super_admin(self):
        return self.account_type == self.COMPANY_SUPER_ADMIN

    @property
    def is_company_sub_admin(self):
        return self.account_type == self.COMPANY_SUB_ADMIN