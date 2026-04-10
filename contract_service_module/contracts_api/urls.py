from django.urls import path
from .views.contractTypeViews import ContractTypeView
from .views.contractTemplateViews import ContractTemplateView
from .views.employeContractViews import EmployeeContractView

urlpatterns = [
    # Contract Types
    path('types/', ContractTypeView.as_view(), name='contract-type'),
    path('types/<int:id>/', ContractTypeView.as_view(), name='contract-type-detail'),
    
    # Contract Templates
    path('templates/', ContractTemplateView.as_view(), name='contract-template'),
    path('templates/<int:id>/', ContractTemplateView.as_view(), name='contract-template-detail'),
    
    # Employee Contracts
    path('employee-contracts/', EmployeeContractView.as_view(), name='employee-contract'),
    path('employee-contracts/<int:id>/', EmployeeContractView.as_view(), name='employee-contract-detail'),
]
