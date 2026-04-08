from django.urls import path
from .views.meeting_views import MeetingListView, MeetingDetailsView
from .views.meeting_room_views import MeetingRoomListView, MeetingRoomDetailsView
from .views.meeting_type_views import MeetingTypeListView, MeetingTypeDetailsView
from .views.attendee_views import AttendeeListView, AttendeeDetailsView
from .views.minutes_views import MinutesListView, MinutesDetailsView
from .views.action_item_views import ActionItemListView, ActionItemDetailsView
from .views.auth_views import LoginView

urlpatterns = [
    # Auth
    path('auth/login/', LoginView.as_view(), name='auth-login'),

    # Meetings
    path('meetings/', MeetingListView.as_view(), name='meeting-list'),
    path('meetings/<int:id>/', MeetingDetailsView.as_view(), name='meeting-detail'),
    
    # Meeting Types
    path('meeting-types/', MeetingTypeListView.as_view(), name='type-list'),
    
    # Meeting Rooms
    path('meeting-rooms/', MeetingRoomListView.as_view(), name='room-list'),
    path('meeting-rooms/<int:id>/', MeetingRoomDetailsView.as_view(), name='room-detail'),
    
    # Attendees
    path('meeting-attendees/', AttendeeListView.as_view(), name='attendee-list'),
    
    # Minutes
    path('meeting-minutes/', MinutesListView.as_view(), name='minutes-list'),
    
    # Action Items
    path('action-items/', ActionItemListView.as_view(), name='action-item-list'),
    path('action-items/<int:id>/', ActionItemDetailsView.as_view(), name='action-item-detail'),
]
