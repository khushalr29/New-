from django.urls import path
from .views.branchView import BranchView, ActiveBranchView, BranchStatusToggleView
from .views.departmentsView import DepartmentView, ActiveDepartmentView, DepartmentStatusToggleView
from .views.designationsView import DesignationView, ActiveDesignationView, DesignationStatusToggleView
from .views.documentTypeView import DocumentTypeView
from .views.employeeView import EmployeeView, ActiveEmployeeView
from .views.trainingView import TrainingProgramView, AssignTrainingView, TrainingSessionView, TrainingTypeView
from .views.transferView import TransferView
from .views.promotionsView import PromotionsView
from .views.terminationsView import TerminationsView
from .views.awardsView import AwardView
from .views.performanceView import IndicatorCategoryView, IndicatorView, GoalTypeView, ReviewCycleView, EmployeeReviewView, EmployeeGoalView
from .views.awardTypeView import AwardTypeView
from .views.resignationsView import ResignationView
from .views.holidayView import HolidayView
from .views.tripsView import TripsView
from .views.warningView import WarningView
from .views.assetManagementView import AssetTypeView, AssetView
from .views.announcementView import AnnouncementView
from .views.complaintsView import ComplaintsView

urlpatterns = [
    path('branches', BranchView.as_view()),
    path('branches/<int:id>', BranchView.as_view()),
    path('branches/active', ActiveBranchView.as_view()),
    path('branches/<int:id>/toggle-status', BranchStatusToggleView.as_view()),

    path('departments', DepartmentView.as_view()),
    path('departments/<int:id>', DepartmentView.as_view()),
    path('departments/active', ActiveDepartmentView.as_view()),
    path('departments/<int:id>/toggle-status', DepartmentStatusToggleView.as_view()),

    path('designation', DesignationView.as_view()),
    path('designation/<int:id>', DesignationView.as_view()),
    path('designation/active', ActiveDesignationView.as_view()),
    path('designation/status-toggle/<int:id>', DesignationStatusToggleView.as_view()),

    path('document-type', DocumentTypeView.as_view()),
    path('document-type/<int:id>', DocumentTypeView.as_view()),

    path('employee', EmployeeView.as_view()),
    path('employee/<int:id>', EmployeeView.as_view()),
    path('employee/active', ActiveEmployeeView.as_view()),

    path('asset-type', AssetTypeView.as_view()),
    path('asset-type/<int:id>', AssetTypeView.as_view()),
    path('asset', AssetView.as_view()),
    path('asset/<int:id>', AssetView.as_view()),

    path('training-type', TrainingTypeView.as_view()),
    path('training-type/<int:id>', TrainingTypeView.as_view()),
    path('training-program', TrainingProgramView.as_view()),
    path('training-program/<int:id>', TrainingProgramView.as_view()),
    path('training-session', TrainingSessionView.as_view()),
    path('training-session/<int:id>', TrainingSessionView.as_view()),
    path('assign-training', AssignTrainingView.as_view()),
    path('assign-training/<int:id>', AssignTrainingView.as_view()),

    path('award-type', AwardTypeView.as_view()),
    path('award-type/<int:id>', AwardTypeView.as_view()),
    path('awards', AwardView.as_view()),
    path('awards/<int:id>', AwardView.as_view()),

    path('resignations', ResignationView.as_view()),
    path('resignations/<int:id>', ResignationView.as_view()),

    path('holiday', HolidayView.as_view()),
    path('holiday/<int:id>', HolidayView.as_view()),

    path('trips', TripsView.as_view()),
    path('trips/<int:id>', TripsView.as_view()),

    path('warning', WarningView.as_view()),
    path('warning/<int:id>', WarningView.as_view()),

    path('announcement', AnnouncementView.as_view()),
    path('announcement/<int:id>', AnnouncementView.as_view()),

    path('complaints', ComplaintsView.as_view()),
    path('complaints/<int:id>', ComplaintsView.as_view()),

    path('indicator-category', IndicatorCategoryView.as_view()),
    path('indicator-category/<int:id>', IndicatorCategoryView.as_view()),
    path('indicator', IndicatorView.as_view()),
    path('indicator/<int:id>', IndicatorView.as_view()),
    path('goal-types', GoalTypeView.as_view()),
    path('goal-types/<int:id>', GoalTypeView.as_view()),
    path('employee-goals', EmployeeGoalView.as_view()),
    path('employee-goals/<int:id>', EmployeeGoalView.as_view()),
    path('review-cycles', ReviewCycleView.as_view()),
    path('review-cycles/<int:id>', ReviewCycleView.as_view()),
    path('employee-reviews', EmployeeReviewView.as_view()),
    path('employee-reviews/<int:id>', EmployeeReviewView.as_view()),

    path('transfers', TransferView.as_view()),
    path('transfers/<int:id>', TransferView.as_view()),

    path('promotions', PromotionsView.as_view()),
    path('promotions/<int:id>', PromotionsView.as_view()),

    path('terminations', TerminationsView.as_view()),
    path('terminations/<int:id>', TerminationsView.as_view())
]