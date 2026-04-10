from django.urls import path
from .views.leaveTypeViews import LeaveTypeView
from .views.leavePolicyViews import LeavePolicyView
from .views.leaveBalanceViews import LeaveBalanceView
from .views.leaveApplicationViews import LeaveApplicationView

urlpatterns = [
    # Leave Type URLs
    path('leave-types/', LeaveTypeView.as_view(), name='leavetype'),
    path('leavetypedetails/<int:id>/', LeaveTypeView.as_view(), name='leavetype-details'),

    # Leave Policy URLs
    path('leave-policies/', LeavePolicyView.as_view(), name='leavepolicy'),
    path('leavepolicydetails/<int:id>/', LeavePolicyView.as_view(), name='leavepolicy-details'),

    # Leave Balance URLs
    path('leave-balances/', LeaveBalanceView.as_view(), name='leavebalance'),
    path('leavebalancedetails/<int:id>/', LeaveBalanceView.as_view(), name='leavebalance-details'),

    # Leave Application URLs
    path('leave-applications/', LeaveApplicationView.as_view(), name='leaveapplication'),
    path('leaveapplicationdetails/<int:id>/', LeaveApplicationView.as_view(), name='leaveapplication-details'),
]
