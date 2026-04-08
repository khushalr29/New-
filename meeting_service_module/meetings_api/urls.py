from django.urls import path
from .views.meetingviews import MeetingListView, MeetingDetailsView
from .views.meetingRoomviews import MeetingRoomListView, MeetingRoomDetailsView
from .views.meetingTypeviews import MeetingTypeListView, MeetingTypeDetailsView
from .views.meetingAttendeeviews import AttendeeListView, AttendeeDetailsView
from .views.meetingMinutes import MinutesListView, MinutesDetailsView
from .views.actionitemviews import ActionItemListView, ActionItemDetailsView

urlpatterns = [
    # Meetings
    path('meetings/', MeetingListView.as_view(), name='meeting-list'),
    path('meetings/<int:id>/', MeetingDetailsView.as_view(), name='meeting-detail'),
    
    # Meeting Types
    path('meeting-types/', MeetingTypeListView.as_view(), name='type-list'),
    path('meetingtypedetails/<int:id>/', MeetingTypeDetailsView.as_view(), name = 'meeting-details'),
    
    # Meeting Rooms
    path('meeting-rooms/', MeetingRoomListView.as_view(), name='room-list'),
    path('meeting-rooms/<int:id>/', MeetingRoomDetailsView.as_view(), name='room-detail'),
    
    # Attendees
    path('meeting-attendees/', AttendeeListView.as_view(), name='attendee-list'),
    path('meeting-attendees/<int:id>/', AttendeeDetailsView.as_view(), name='attendee-detail'),
    
    # Minutes
    path('meeting-minutes/', MinutesListView.as_view(), name='minutes-list'),
    path('meeting-minutes/<int:id>/', MinutesDetailsView.as_view(), name='minutes-detail'),
    
    # Action Items
    path('action-items/', ActionItemListView.as_view(), name='action-item-list'),
    path('action-items/<int:id>/', ActionItemDetailsView.as_view(), name='action-item-detail'),
]
