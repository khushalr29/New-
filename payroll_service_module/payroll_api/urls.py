from django.urls import path
from .views.payrollrunsViews import PayrollRunView
from .views.salaryComponentViews import SalaryComponentView

urlpatterns = [
    path('payroll-runs/', PayrollRunView.as_view(), name='payroll-runs'),
    path('payroll-runs/<int:id>/', PayrollRunView.as_view(), name='payroll-runs-detail'),
    path('salary-components/', SalaryComponentView.as_view(), name='salary-components'),
    path('salary-components/<int:id>/', SalaryComponentView.as_view(), name='salary-components-detail'),
]
