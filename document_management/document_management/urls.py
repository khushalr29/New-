from django.contrib import admin
from django.urls import path, include
from django.views.generic import TemplateView

urlpatterns = [
    path("admin/", admin.site.urls),
    path('api/v1/document/', include('document.urls')),
    path('swagger/', TemplateView.as_view(template_name='swagger.html'), name='swagger'),
]
