from django.urls import path
from .views.branchView import BranchView, ActiveBranchView, BranchStatusToggleView
from .views.departmentsView import DepartmentView, ActiveDepartmentView, DepartmentStatusToggleView
from .views.designationsView import DesignationView, ActiveDesignationView, DesignationStatusToggleView
from .views.documentTypeView import DocumentTypeView
from .views.employeeView import EmployeeView, ActiveEmployeeView

urlpatterns = [
    path('branch', BranchView.as_view()),
    path('branch/<int:id>', BranchView.as_view()),
    path('branch/active', ActiveBranchView.as_view()),
    path('branch/status/<int:id>', BranchStatusToggleView.as_view()),

    path('department', DepartmentView.as_view()),
    path('department/<int:id>', DepartmentView.as_view()),
    path('department/active', ActiveDepartmentView.as_view()),
    path('department/status/<int:id>', DepartmentStatusToggleView.as_view()),

    path('designation', DesignationView.as_view()),
    path('designation/<int:id>', DesignationView.as_view()),
    path('designation/active', ActiveDesignationView.as_view()),
    path('designation/status/<int:id>', DesignationStatusToggleView.as_view()),

    path('document-type', DocumentTypeView.as_view()),
    path('document-type/<int:id>', DocumentTypeView.as_view()),

    path('employee', EmployeeView.as_view()),
    path('employee/<int:id>', EmployeeView.as_view()),
    path('employee/active', ActiveEmployeeView.as_view()),
]