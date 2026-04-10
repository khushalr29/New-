from django.contrib import admin
from django.urls import path, include
from django.views.generic import TemplateView

urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/v1/auth/", include("auth.urls")),
    path("api/v1/company-employee/", include("company_employee.urls")),
    path("swagger/", TemplateView.as_view(template_name="swagger.html"), name="swagger"),
]
