from django.urls import path
from .views.meetingviews import MeetingView
from .views.meetingRoomviews import MeetingRoomView
from .views.meetingTypeviews import MeetingTypeView
from .views.meetingAttendeeviews import MeetingAttendeeView
from .views.meetingMinutes import MeetingMinutesView
from .views.actionitemviews import ActionItemView

urlpatterns = [
    # Meetings
    path('meetings/', MeetingView.as_view(), name='meeting'),
    path('meetings/<int:id>/', MeetingView.as_view(), name='meeting-detail'),
    
    # Meeting Types
    path('meeting-types/', MeetingTypeView.as_view(), name='type'),
    path('meetingtypedetails/<int:id>/', MeetingTypeView.as_view(), name = 'meeting-details'),
    
    # Meeting Rooms
    path('meeting-rooms/', MeetingRoomView.as_view(), name='room'),
    path('meeting-rooms/<int:id>/', MeetingRoomView.as_view(), name='room-detail'),
    
    # Attendees
    path('meeting-attendees/', MeetingAttendeeView.as_view(), name='attendee'),
    path('meeting-attendees/<int:id>/', MeetingAttendeeView.as_view(), name='attendee-detail'),
    
    # Minutes
    path('meeting-minutes/', MeetingMinutesView.as_view(), name='minutes'),
    path('meeting-minutes/<int:id>/', MeetingMinutesView.as_view(), name='minutes-detail'),
    
    # Action Items
    path('action-items/', ActionItemView.as_view(), name='action-item'),
    path('action-items/<int:id>/', ActionItemView.as_view(), name='action-item-detail'),
]
