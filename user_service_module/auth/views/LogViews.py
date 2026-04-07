from rest_framework.views import APIView
from shared.models import UserActivityLog,User
from django.contrib.admin.models import LogEntry
from shared.utils.common import paginate_queryset
from shared.utils.response import ResponseHandler,ResponseMessages

class RecentAdminActionsAPIView(APIView):

    def get(self, request, *args, **kwargs):
        user = request.user

        if user.is_superuser:
            logs = LogEntry.objects.select_related('user', 'content_type').order_by('-action_time')[:10000]
            activity_logs = UserActivityLog.objects.select_related('user').order_by('-timestamp')[:10000]
        else:
            user_company = getattr(user, 'company', None)
            if not user_company:
                return ResponseHandler.bad_request(message=ResponseMessages.USER_NOT_FOUND)

            users_in_company = User.objects.filter(company=user_company)
            user_ids = users_in_company.values_list('id', flat=True)

            logs = LogEntry.objects.select_related('user', 'content_type').filter(user_id__in=user_ids).order_by('-action_time')[:10000]
            activity_logs = UserActivityLog.objects.select_related('user').filter(company=user_company).order_by('-timestamp')[:10000]

        recent_actions = []

        for log in logs:
            action_flag = {
                1: "Added",
                2: "Changed",
                3: "Deleted"
            }.get(log.action_flag, "Unknown")

            recent_actions.append({
                "action": action_flag,
                "user": log.user.email if log.user else None,
                "content_type": log.content_type.model if log.content_type else None,
                "object_repr": log.object_repr,
                "change_message": log.change_message,
                "action_time": log.action_time.isoformat(),
                "type": "admin_log",
            })

        for act in activity_logs:
            recent_actions.append({
                "action": act.action.capitalize(),
                "user": act.user.email if act.user else None,
                "content_type": act.resource,
                "object_repr": str(act.resource_id) if act.resource_id else None,
                "change_message": None,
                "action_time": act.timestamp.isoformat(),
                "type": "user_activity",
                "status": act.status.capitalize() if act.status else None,
                "company": act.company.id if act.company else None,
            })

        recent_actions.sort(key=lambda x: x['action_time'], reverse=True)
        return paginate_queryset(recent_actions, request, view=self)
