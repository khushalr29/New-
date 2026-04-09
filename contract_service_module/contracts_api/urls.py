from django.urls import path
from .views.contractTypeViews import ContractTypeListView, ContractTypeDetailView
from .views.contractTemplateViews import ContractTemplateListView, ContractTemplateDetailView
from .views.employeContractViews import EmployeeContractListView, EmployeeContractDetailView

urlpatterns = [
    # Contract Types
    path('types/', ContractTypeListView.as_view(), name='contract-type-list'),
    path('types/<int:pk>/', ContractTypeDetailView.as_view(), name='contract-type-detail'),
    
    # Contract Templates
    path('templates/', ContractTemplateListView.as_view(), name='contract-template-list'),
    path('templates/<int:pk>/', ContractTemplateDetailView.as_view(), name='contract-template-detail'),
    
    # Employee Contracts
    path('employee-contracts/', EmployeeContractListView.as_view(), name='employee-contract-list'),
    path('employee-contracts/<int:pk>/', EmployeeContractDetailView.as_view(), name='employee-contract-detail'),
]
