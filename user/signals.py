from django.dispatch import receiver
from django.contrib.auth.signals import user_logged_in
from django.core.cache import cache
from .models import UserLoginActivity
import logging
from django.utils import timezone

error_log = logging.getLogger('error')

# Helper function to get client IP
def get_client_ip(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip

@receiver(user_logged_in)
def log_user_logged_in_success(sender, user, request, **kwargs):
    # No need to reassign user from request.user, use the provided `user` argument
    ct = cache.get('count', 0, version=user.username)
    newcount = ct + 1
    cache.set('count', newcount, 60 * 60 * 24 * 365, version=user.username)

    request.session['last_login'] = str(timezone.now())

    try:
        # Fetch user agent info without creating a tuple
        user_agent_info = request.META.get('HTTP_USER_AGENT', '<unknown>')[:255]
        login_time = timezone.now()

        login_count = cache.get('count', version=user.username)

        user_login_activity_log = UserLoginActivity(
            login_IP=get_client_ip(request),
            login_datetime=login_time,
            login_num=login_count,
            login_username=user.username,
            user_agent_info=user_agent_info,
            status=UserLoginActivity.SUCCESS
        )
        user_login_activity_log.save()

    except Exception as e:
        error_log.error(f"log_user_logged_in request: {request}, error: {e}")
