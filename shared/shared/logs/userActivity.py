import platform
import socket
import getpass
import time
from uuid import uuid4
from django.utils.timezone import now
from ..models import UserActivityLog

def _get_ip_address():
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))
        ip_address = s.getsockname()[0]
        s.close()
        return ip_address
    except Exception:
        return "Unable to determine IP address"
    
def get_system_details():
    system_info = {
        "OS": platform.system(),
        "Hostname": socket.gethostname(),
        "IP Address": _get_ip_address(),
        "System User": getpass.getuser()
    }
    return system_info

def get_client_ip(request):
    print(request.META)
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip

def log_user_activity(user, action, resource=None, resource_id=None, status='success', request=None, response=None):
    if user and user.is_authenticated:
        company_id = getattr(user, 'company', None)
        client_ip = get_client_ip(request) if request else None
        
        request_method = request.method if request else None
        endpoint = request.path if request else None
        user_agent = request.META.get('HTTP_USER_AGENT') if request else None
        request_data = request.data if request else None
        response_data = response.data if response else None
        execution_time = None
        tracing_id = uuid4()
        
        if request:
            start_time = time.time()
            execution_time = time.time() - start_time

        system_info = get_system_details()

        UserActivityLog.objects.create(
            user=user,
            action=action,
            resource=resource,
            resource_id=resource_id,
            status=status,
            company=company_id,
            client_ip=client_ip,
            tracing_id=tracing_id,
            request_method=request_method,
            endpoint=endpoint,
            request_data=request_data,
            response_data=response_data,
            execution_time=execution_time,
            user_agent=user_agent,
            system_info=system_info,
            timestamp=now()
        )
