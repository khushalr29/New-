from django.urls import path
from .views.attendancePolicyView import AttendancePolicyView
from .views.attendanceRecordsView import AttendanceRecordsView
from .views.attendanceRegularizationView import AttendanceRegularizationView
from .views.shiftView import ShiftView

urlpatterns = [
    path('shift', ShiftView.as_view(), name='shift'),
    path('shift/<int:id>', ShiftView.as_view(), name='shift'),
    
    path('attendance-policy', AttendancePolicyView.as_view(), name='attendance-policy'),
    path('attendance-policy/<int:id>', AttendancePolicyView.as_view(), name='attendance-policy'),
    
    path('attendance-records', AttendanceRecordsView.as_view(), name='attendance-records'),
    path('attendance-records/<int:id>', AttendanceRecordsView.as_view(), name='attendance-records'),
    
    path('attendance-regularization', AttendanceRegularizationView.as_view(), name='attendance-regularization'),
    path('attendance-regularization/<int:id>', AttendanceRegularizationView.as_view(), name='attendance-regularization'),
]