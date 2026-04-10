from django.urls import path
from .views.timeEntryViews import TimeEntryView

urlpatterns = [
    path('time-entries/', TimeEntryView.as_view(), name='time-entries'),
    path('time-entries/<int:id>/', TimeEntryView.as_view(), name='time-entry-detail'),
]

