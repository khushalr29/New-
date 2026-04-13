from django.urls import path
from .views.branchView import BranchView, ActiveBranchView, BranchStatusToggleView
from .views.departmentsView import DepartmentView, ActiveDepartmentView, DepartmentStatusToggleView

urlpatterns = [
    path('branch', BranchView.as_view()),
    path('branch/<int:id>', BranchView.as_view()),
    path('branch/active', ActiveBranchView.as_view()),
    path('branch/status/<int:id>', BranchStatusToggleView.as_view()),

    path('department', DepartmentView.as_view()),
    path('department/<int:id>', DepartmentView.as_view()),
    path('department/active', ActiveDepartmentView.as_view()),
    path('department/status/<int:id>', DepartmentStatusToggleView.as_view()),
]