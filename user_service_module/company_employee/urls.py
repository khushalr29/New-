from django.urls import path
from .views.companyView import CompanyView, CompanyStatusToggleView
from .views.employeeView import EmployeeView, EmployeeStatusToggleView
from .views.planView import PlanView
from .views.subscriptionView import SubscriptionView
from .views.roleView import RoleView

urlpatterns = [
    # Company paths
    path('companies', CompanyView.as_view(), name='company-list-create'),
    path('companies/<int:pk>', CompanyView.as_view(), name='company-detail'),
    path('companies/status/<int:pk>', CompanyStatusToggleView.as_view(), name='company-status-toggle'),
    
    # Employee paths
    path('employees', EmployeeView.as_view(), name='employee-list-create'),
    path('employees/<int:pk>', EmployeeView.as_view(), name='employee-detail'),
    path('employees/status/<int:pk>', EmployeeStatusToggleView.as_view(), name='employee-status-toggle'),
    
    # Plan paths
    path('plans', PlanView.as_view(), name='plan-list'),
    path('plans/<int:pk>', PlanView.as_view(), name='plan-detail'),
    
    # Subscription paths
    path('subscriptions', SubscriptionView.as_view(), name='subscription-list-create'),
    path('subscriptions/<int:pk>', SubscriptionView.as_view(), name='subscription-detail'),

    # Role paths
    path('roles', RoleView.as_view(), name='role-list-create'),
    path('roles/<int:pk>', RoleView.as_view(), name='role-detail'),
]
