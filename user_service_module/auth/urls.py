from django.urls import path
from .views.enumView import EnumListView
from .views.LogViews import RecentAdminActionsAPIView
from rest_framework_simplejwt.views import TokenRefreshView
from .views.sessionUserTypeView import SessionUserTypeView
from .views.permissionView import PermissionListView,PermissionDetailView,ManagePermissionsForUserView,UserPermissionsListView
from .views.userView import UserCreationView,UserListView,UserUpdationView,UserDetailView,UserDeleteView,UserProfileView,ChangeUserStatusView,EnabledUserListView
from .views.authView import UserLoginView,UserLogoutView,SetPasswordView,SendPasswordResetEmailView,ImpersonationLoginView,CheckDomainExistenceView,SetMPinView,CheckMPinView,VerifyPasswordView
from .views.groupPermissionView import GroupCreateView,GroupListView,ManagePermissionsForGroupView,GroupDetailView,ManageUserGroupView,GroupDeleteView,ChangeGroupStatusView,EnabledGroupListView

urlpatterns = [
    # User Related path
    path('creates',UserCreationView.as_view(),name='createuser'),
    path('updates/<int:id>',UserUpdationView.as_view(),name='updateuser'),
    path('details/<int:id>',UserDetailView.as_view(),name='getuser'),
    path('profiles',UserProfileView.as_view(), name='profile'),
    path('lists',UserListView.as_view(),name='list'),
    path('deletes',UserDeleteView.as_view(),name='deleteuser'),
    path('status/<int:id>',ChangeUserStatusView.as_view(), name='user-status'),
    path('enabled-users', EnabledUserListView.as_view(), name='enabled-users-list'),
    path('set-mpins', SetMPinView.as_view(), name='set-mpin'),
    path('check-mpins', CheckMPinView.as_view(), name='check-mpin'),
    # Auth path
    path('logins',UserLoginView.as_view(), name='login'),
    path('impersonation-logins', ImpersonationLoginView.as_view(), name='sso_login_as'),
    path('refreshtokens',TokenRefreshView.as_view(),name='refresh-token'),
    path('logouts',UserLogoutView.as_view(), name='login'),
    path('send-reset-password-emails',SendPasswordResetEmailView.as_view(), name='reset-password'),
    path('setpassword/<str:uid>/<str:token>',SetPasswordView.as_view(), name='setpassword'),
    path('check-domains',CheckDomainExistenceView.as_view(), name='domain'),
    path('verify-passwords', VerifyPasswordView.as_view(), name='verify-password'),
    # permission
    path('all-permissions', PermissionListView.as_view(), name='permission-list'),
    path('get-permissions/<int:id>', PermissionDetailView.as_view(), name='permission-detail'),
    path('manage-permissions/<int:id>',ManagePermissionsForUserView.as_view(),name='manage-permissoion'),
    path('permissions/<int:id>', UserPermissionsListView.as_view(), name='user-permissions'),
    # group
    path('groups-create',GroupCreateView.as_view(), name='create-group'),
    path('groups-list', GroupListView.as_view(), name='group-list'),
    path('groups-detail/<int:id>', GroupDetailView.as_view(), name='group-detail'),
    path('groups-delete',GroupDeleteView.as_view(), name='delete-group'),
    path('groups-permissions-update/<int:id>',ManagePermissionsForGroupView.as_view(), name='manage-permission'),
    path('manage-groups/<int:id>',ManageUserGroupView.as_view(), name='manage-group'),
    path('groups-status-update/<int:id>', ChangeGroupStatusView.as_view(), name='group-status-update'),
    path('enabled-groups-list', EnabledGroupListView.as_view(), name='enabled-group-list'),
    # enum
    path('enums',EnumListView.as_view(),name='enum'),
    #session user type
    path('session-user-types',SessionUserTypeView.as_view(), name='session-user-type'),
    path('recent-actions', RecentAdminActionsAPIView.as_view(), name='admin-recent-actions')

]