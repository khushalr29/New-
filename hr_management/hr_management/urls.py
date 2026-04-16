from django.contrib import admin
from django.urls import path, include
from django.views.generic import TemplateView
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path("admin/", admin.site.urls),
    path('api/v1/auth/', include('management.urls')),
    path('api/v1/auth/', include('auth.urls')),
    path('api/v1/company-employee/', include('company_employee.urls')),
    path('swagger/', TemplateView.as_view(template_name='swagger.html'), name='swagger-ui'),
] + static(settings.STATIC_URL, document_root=settings.STATICFILES_DIRS[0])
