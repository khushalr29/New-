from datetime import date
from django.db import models
from zoneinfo import available_timezones
from django.utils import timezone
from .static import Country, City,State
from django.contrib.auth.models import Permission
from ...utils.subscriptionEnddate import get_subscription_end_date
from ...utils.common import validate_address,validate_char_field,validate_integer_field,validate_name, validate_domain
from .enums import Gender,AddsOnServices,PaymentMode,PaymentStatus

from .base import BaseModel

class Plan(BaseModel):
    plan_name = models.CharField(max_length=255, validators=[validate_name])
    plan_price_inr = models.DecimalField(max_digits=10, decimal_places=2)
    plan_price_usd = models.DecimalField(max_digits=10, decimal_places=2)
    no_of_users = models.PositiveIntegerField(validators=[validate_integer_field])
    no_of_employees = models.PositiveIntegerField(validators=[validate_integer_field])
    payment_duration = models.CharField(max_length=20, blank=True,validators=[validate_char_field])
    feature = models.JSONField(blank=True, null=True)
    description = models.TextField()
    visible_to_user = models.BooleanField(default=True)
    permissions= models.ManyToManyField(Permission, blank=True)

    def __str__(self):
        return self.plan_name

class Company(BaseModel):
    company_name = models.CharField(max_length=255)
    company_code = models.CharField(max_length=50,validators=[validate_char_field])
    company_type = models.ForeignKey('shared.CompanyType', on_delete=models.CASCADE, related_name='companies')
    logo = models.TextField(blank=True)
    established_date = models.DateField(null=True, blank=True)
    about_company = models.TextField()
    client_name = models.CharField(max_length=100,validators=[validate_name])
    client_designation = models.CharField(max_length=255,validators=[validate_char_field])
    country_number_code = models.PositiveIntegerField(default=91,validators=[validate_integer_field])
    client_number = models.CharField(max_length=20)
    client_email = models.EmailField()
    client_gender = models.CharField(max_length=20,choices=Gender.choices,validators=[validate_char_field])
    website = models.TextField(max_length=255, blank=True)
    address_line_1 = models.CharField(max_length=255,validators=[validate_address])
    address_line_2 = models.CharField(max_length=255, blank=True,validators=[validate_address])
    country = models.ForeignKey(Country, on_delete=models.CASCADE, blank=True,null=True)
    state = models.ForeignKey(State, on_delete=models.CASCADE, blank=True,null=True)
    city = models.ForeignKey(City, on_delete=models.CASCADE, blank=True,null=True)
    pincode = models.CharField(max_length=6,validators=[validate_char_field])
    no_of_floors = models.PositiveIntegerField(blank=True, null=True,validators=[validate_integer_field])
    no_of_blocks = models.PositiveIntegerField(blank=True, null=True,validators=[validate_integer_field])
    no_of_rooms = models.PositiveIntegerField(blank=True, null=True,validators=[validate_integer_field])
    special_features = models.TextField(blank=True)
    allow_plan_renewal_on_same_price = models.BooleanField(default=True)
    bill_me = models.CharField(max_length=20, default='Monthly')
    plan_type = models.ForeignKey('Plan', on_delete=models.CASCADE, blank=True, null=True)
    adds_on_services = models.CharField(max_length=255, choices=AddsOnServices.choices, blank=True, null=True)
    plan_activation_date = models.DateField(null=True, blank=True)
    subscription_end_date = models.DateField(null=True, blank=True)
    no_of_users = models.PositiveIntegerField(validators=[validate_integer_field])
    no_of_employees = models.PositiveIntegerField(validators=[validate_integer_field])
    payment_mode = models.CharField(max_length=20,choices=PaymentMode.choices,default='online',validators=[validate_char_field])
    payment_status = models.CharField(max_length=20,choices=PaymentStatus.choices,validators=[validate_char_field])
    amount_paid = models.DecimalField(max_digits=10, decimal_places=2)
    sub_domain = models.CharField(max_length=255, validators=[validate_domain])
    timezone = models.CharField(
        max_length=100,
        default='Asia/Kolkata',
        choices=[(tz, tz) for tz in sorted(available_timezones())]
    )

    def save(self, *args, **kwargs):
        if self.plan_type:
            if not self.plan_activation_date:
                self.plan_activation_date = date.today()
            if not self.subscription_end_date:
                self.subscription_end_date = get_subscription_end_date(
                    self.plan_activation_date,
                    self.plan_type.payment_duration
                )
        super().save(*args, **kwargs)
    
    @property
    def full_domain(self):
        return f"www.{self.sub_domain}.hrms.in"

    def is_subscription_active(self):
        return self.subscription_end_date and self.subscription_end_date >= timezone.now().date()

    def __str__(self):
        return self.company_name

class Subscription(BaseModel):
    company = models.ForeignKey(Company, on_delete=models.CASCADE)
    plan_type = models.ForeignKey(Plan, on_delete=models.CASCADE,blank=True)
    amount_paid = models.DecimalField(max_digits=10, decimal_places=2)
    plan_activation_date = models.DateField(null=True, blank=True)
    subscription_end_date = models.DateField(null=True, blank=True)
    payment_mode = models.CharField(max_length=20,choices=PaymentMode.choices,blank=True,validators=[validate_char_field])
    remarks = models.TextField(blank=True, null=True)
    transaction_ref_no = models.CharField(max_length=255)
    status = models.CharField(max_length=50, choices=PaymentStatus.choices)
    gateway = models.CharField(max_length=50)
    gateway_response = models.JSONField(blank=True, null=True)
    currency = models.CharField(max_length=3, default='INR')

    def __str__(self):
        return f"{self.company} ({self.transaction_ref_no})"
