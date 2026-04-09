from django.urls import path
from .views.leaveTypeViews import LeaveTypeListView, LeaveTypeDetailsView
from .views.leavePolicyViews import LeavePolicyListView, LeavePolicyDetailsView
from .views.leaveBalanceViews import LeaveBalanceListView, LeaveBalanceDetailsView
from .views.leaveApplicationViews import LeaveApplicationListView, LeaveApplicationDetailsView

urlpatterns = [
    # Leave Type URLs
    path('leave-types/', LeaveTypeListView.as_view(), name='leavetype-list'),
    path('leavetypedetails/<int:id>/', LeaveTypeDetailsView.as_view(), name='leavetype-details'),

    # Leave Policy URLs
    path('leave-policies/', LeavePolicyListView.as_view(), name='leavepolicy-list'),
    path('leavepolicydetails/<int:id>/', LeavePolicyDetailsView.as_view(), name='leavepolicy-details'),

    # Leave Balance URLs
    path('leave-balances/', LeaveBalanceListView.as_view(), name='leavebalance-list'),
    path('leavebalancedetails/<int:id>/', LeaveBalanceDetailsView.as_view(), name='leavebalance-details'),

    # Leave Application URLs
    path('leave-applications/', LeaveApplicationListView.as_view(), name='leaveapplication-list'),
    path('leaveapplicationdetails/<int:id>/', LeaveApplicationDetailsView.as_view(), name='leaveapplication-details'),
]
