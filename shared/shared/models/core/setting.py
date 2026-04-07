from django.db import models
from ..core.static import Currency
from ..core.enums import (LanguageEnum, DateFormatEnum, TimeFormatEnum, TimeZone, 
                        SidebarVarientEnum, SidebarStyleEnum, LayoutDirectionEnum, 
                        ThemeModeEnum, SymbolPositionEnum, DecimalSeparatorEnum, ThousandsSeparatorEnum,
                        EmailProvider, SmtpEncryption, DocumentTemplateType, StorageDriver, CacheDriver, FileTypeEnum)

class SystemSetting(models.Model):
    default_language = models.CharField(max_length=20,choices=LanguageEnum.choices, default=LanguageEnum.ENGLISH)
    date_format = models.CharField(max_length=20, choices = DateFormatEnum.choices,default= DateFormatEnum.Y_M_D )
    time_format = models.CharField(max_length = 20 , choices=TimeFormatEnum.choices, default=TimeFormatEnum.H_I)
    default_timezone = models.CharField(max_length=50,choices=TimeZone.choices, default=TimeZone.UTC)
    ip_restriction = models.BooleanField(default=False)

class BrandSetting(models.Model):    
    logo_dark = models.TextField(null=True, blank=True)
    logo_light = models.TextField(null =True, blank=True)
    favicon = models.TextField(null=True, blank=True)
    title_text = models.CharField(max_length=255, null=True, blank=True)
    footer_text = models.CharField(max_length=255, null=True, blank=True)
    company_mobile_no = models.CharField(max_length=15, null=True, blank=True)
    company_address = models.TextField(null=True, blank=True)
    theme_color = models.CharField(max_length=7 , default='#10b931')
    sidebar_variant = models.CharField(max_length=15, choices=SidebarVarientEnum.choices, default = SidebarVarientEnum.INSET)
    sidebar_style = models.CharField(max_length=15, choices =SidebarStyleEnum.choices, default = SidebarStyleEnum.PLAIN)
    layout_direction = models.CharField(max_length=15, choices =LayoutDirectionEnum.choices, default=LayoutDirectionEnum.LEFT_TO_RIGHT)
    theme_mode = models.CharField(max_length=15, choices=ThemeModeEnum.choices, default = ThemeModeEnum.LIGHT)

class CurrencySetting(models.Model):
    currency_amount = models.DecimalField(max_digits=20, decimal_places=4, default=0.00)
    default_currency = models.ForeignKey(Currency, on_delete=models.CASCADE, related_name= 'currency')
    currency_symbol = models.CharField(max_length=5, default='$')
    decimal_place = models.PositiveIntegerField(default=2)
    symbol_position = models.CharField(max_length=10 , choices=SymbolPositionEnum.choices, default=SymbolPositionEnum.LEFT)
    decimal_separator = models.CharField(max_length=10, choices=DecimalSeparatorEnum.choices, default = DecimalSeparatorEnum.DOT)
    thousands_separator =models.CharField(max_length=10, choices=ThousandsSeparatorEnum.choices, default = ThousandsSeparatorEnum.COMMA)
    show_decimal = models.BooleanField(default=False)
    add_space = models.BooleanField(default=False)

    class Meta:
        verbose_name = 'Currency Settings'

    def __str__(self):
        return f"Currency — {self.default_currency}"


class EmailSetting(models.Model):
    email_provider = models.CharField(max_length=15, choices=EmailProvider.choices , default=EmailProvider.SMTP)
    mail_driver = models.CharField(max_length=15, choices=EmailProvider.choices , default=EmailProvider.SMTP)
    smtp_host = models.CharField(max_length=255, null= True, blank=True)
    smtp_port = models.CharField(max_length=10, null=True, blank=True)
    smtp_username = models.CharField(max_length=255, null=True, blank=True)
    smtp_password= models.CharField(max_length=255, null=True , blank=True)
    mail_encryption = models.CharField(max_length = 10, choices=SmtpEncryption.choices, default=SmtpEncryption.TLS)
    from_mail = models.EmailField(max_length=255)
    from_name= models.CharField(max_length=255, null=True, blank=True)
    api_key = models.CharField(max_length=255, blank=True)
    mail_domain = models.CharField(max_length=255, blank=True)
    send_test_to = models.EmailField(max_length=255)

class WorkingDaysSetting(models.Model):
    is_monday = models.BooleanField(default=False)
    is_tuesday = models.BooleanField(default=False)
    is_wednesday = models.BooleanField(default=False)
    is_thursday = models.BooleanField(default=False)
    is_friday= models.BooleanField(default=False)
    is_saturday = models.BooleanField(default=False)
    is_sunday = models.BooleanField(default=False)

class IPRestrictionSettings(models.Model):
    is_enabled = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'IP Restriction Settings'

    def __str__(self):
        return f"IP Restriction — {'Enabled' if self.is_enabled else 'Disabled'}"


class AllowedIP(models.Model):
    settings = models.ForeignKey(
        IPRestrictionSettings,
        on_delete=models.CASCADE,
        related_name='allowed_ips'
    )
    ip_address = models.GenericIPAddressField()
    label = models.CharField(max_length=100, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.ip_address} — {self.label}"
    
class ZKTecoSettings(models.Model):
    is_enabled = models.BooleanField(default=False)
    device_ip = models.GenericIPAddressField(null=True, blank=True)
    device_port = models.PositiveIntegerField(default=4370)
    timeout = models.PositiveIntegerField(default=5)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'ZKTeco Settings'

    def __str__(self):
        return f"ZKTeco — {self.device_ip}:{self.device_port}"

class DocumentTemplateSettings(models.Model):
    template_type = models.CharField(
        max_length=30,
        choices=DocumentTemplateType.choices,
        unique=True
    )
    language = models.CharField(max_length=10, default='en')
    template_content = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Document Template Settings'

    def __str__(self):
        return f" ({self.language})"


class StorageSettings(models.Model):
    driver = models.CharField(
        max_length=20,
        choices=StorageDriver.choices,
        default=StorageDriver.LOCAL
    )
    access_key = models.CharField(max_length=255, blank=True)
    secret_key = models.CharField(max_length=255, blank=True)
    bucket_name = models.CharField(max_length=255, blank=True)
    region = models.CharField(max_length=100, blank=True)
    endpoint_url = models.TextField(blank=True)
    base_url = models.TextField(blank=True)
    allowed_file_type = models.CharField(max_length=10, choices = FileTypeEnum.choices)
    max_file_size_mb = models.PositiveIntegerField(default=10)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Storage Settings'

    def __str__(self):
        return f"Storage — {self.driver}"

class ReCaptchaSettings(models.Model):
    is_enabled = models.BooleanField(default=False)
    site_key = models.CharField(max_length=255, blank=True)
    secret_key = models.CharField(max_length=255, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'ReCaptcha Settings'

    def __str__(self):
        return f"ReCaptcha — {'Enabled' if self.is_enabled else 'Disabled'}"

class ChatGPTSettings(models.Model):
    is_enabled = models.BooleanField(default=False)
    api_key = models.CharField(max_length=255, blank=True)
    model_name = models.CharField(max_length=100, default='gpt-3.5-turbo')
    max_tokens = models.PositiveIntegerField(default=1000)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Chat GPT Settings'

    def __str__(self):
        return f"ChatGPT — {self.model_name}"

class CookieSettings(models.Model):
    is_enabled = models.BooleanField(default=False)
    consent_text = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Cookie Settings'

    def __str__(self):
        return f"Cookie — {'Enabled' if self.is_enabled else 'Disabled'}"


class CustomCookieItem(models.Model):
    cookie_settings = models.ForeignKey(
        CookieSettings,
        on_delete=models.CASCADE,
        related_name='custom_cookies'
    )
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    is_required = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

class SEOSettings(models.Model):
    meta_title = models.CharField(max_length=255, blank=True)
    meta_description = models.TextField(blank=True)
    meta_keywords = models.TextField(blank=True)
    og_title = models.CharField(max_length=255, blank=True)
    og_description = models.TextField(blank=True)
    og_image = models.TextField(null=True, blank=True)
    google_analytics_id = models.CharField(max_length=50, blank=True)
    google_tag_manager_id = models.CharField(max_length=50, blank=True)
    robots_txt = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'SEO Settings'

    def __str__(self):
        return f"SEO — {self.meta_title}"

class CacheSettings(models.Model):
    driver = models.CharField(
        max_length=20,
        choices=CacheDriver.choices,
        default=CacheDriver.FILE
    )
    host = models.CharField(max_length=255, default='127.0.0.1')
    port = models.PositiveIntegerField(default=6379)
    password = models.CharField(max_length=255, blank=True)
    database_index = models.PositiveSmallIntegerField(default=0)
    ttl_seconds = models.PositiveIntegerField(default=3600)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Cache Settings'

    def __str__(self):
        return f"Cache — {self.driver}"    


   
