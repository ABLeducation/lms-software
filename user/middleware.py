import logging
from django.utils import timezone
from datetime import timedelta
from .models import UserActivity1
import re
from urllib.parse import urlparse, parse_qs

logger = logging.getLogger(__name__)

class ActivityMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response  # Store the get_response callable

    def __call__(self, request):
        response = self.get_response(request)  # Call the next middleware or view

        if request.user.is_authenticated:
            current_time = timezone.now()
            curriculum_pattern = re.compile(r'^/curriculum/\d+/[^/]+/(?P<lesson_name>[\w-]+)/$')

            try:
                last_activity_str = request.session.get('last_activity', None)
                if last_activity_str:
                    last_activity = timezone.datetime.fromisoformat(last_activity_str).replace(tzinfo=current_time.tzinfo)
                else:
                    last_activity = None

                query_params = parse_qs(urlparse(request.get_full_path()).query)
                action = query_params.get('action', [None])[0]  # Get the 'action' parameter from the query string

                if curriculum_pattern.match(request.path):
                    match = curriculum_pattern.match(request.path)
                    lesson_name = match.group('lesson_name') if match else None

                    if lesson_name:
                        time_spent = current_time - last_activity if last_activity else timedelta(seconds=0)

                        # Create appropriate UserActivity1 record based on action
                        if action == "video":
                            UserActivity1.objects.create(
                                user=request.user,
                                date=current_time,
                                page_visited=lesson_name,
                                video_time_spent=time_spent
                            )
                        elif action == "content":
                            UserActivity1.objects.create(
                                user=request.user,
                                date=current_time,
                                page_visited=lesson_name,
                                content_time_spent=time_spent
                            )
                        elif action == "quiz":
                            UserActivity1.objects.create(
                                user=request.user,
                                date=current_time,
                                page_visited=lesson_name,
                                quiz_time_spent=time_spent
                            )
                        else:
                            # Default behavior for the lesson page
                            UserActivity1.objects.create(
                                user=request.user,
                                date=current_time,
                                page_visited=lesson_name,
                                curriculum_time_spent=time_spent
                            )

                request.session['last_activity'] = current_time.isoformat()

            except Exception as e:
                logger.error(f'Error recording activity for user: {request.user.username}, error: {e}')

        return response


# class ActivityMiddleware:
#     def __init__(self, get_response):
#         self.get_response = get_response

#     def __call__(self, request):
#         response = self.get_response(request)

#         if request.user.is_authenticated:
#             current_time = timezone.now()
#             curriculum_pattern = re.compile(r'^/curriculum/\d+/[^/]+/(?P<lesson_name>[\w-]+)/$')
#             video_pattern = re.compile(r'^/curriculum/\d+/[^/]+/(?P<lesson_name>[\w-]+)/video/$')
#             content_pattern = re.compile(r'^/curriculum/\d+/[^/]+/(?P<lesson_name>[\w-]+)/content/$')
#             quiz_pattern = re.compile(r'^/curriculum/\d+/[^/]+/(?P<lesson_name>[\w-]+)/quiz/$')


#             try:
#                 last_activity_str = request.session.get('last_activity', None)
#                 if last_activity_str:
#                     last_activity = timezone.datetime.fromisoformat(last_activity_str).replace(tzinfo=current_time.tzinfo)
#                 else:
#                     last_activity = None

#                 last_page_visited = request.session.get('last_page_visited', None)

#                 if request.path == '/login/':
#                     UserActivity1.objects.create(
#                         user=request.user,
#                         date=current_time,
#                         login_time=current_time
#                     )

#                 elif request.path == '/user_logout/':
#                     try:
#                         last_login_activity = UserActivity1.objects.filter(user=request.user, logout_time__isnull=True).order_by('-login_time').first()

#                         if last_login_activity:
#                             last_login_activity.logout_time = current_time
#                             last_login_activity.time_spent = current_time - last_login_activity.login_time
#                             last_login_activity.save()
#                         else:
#                             logger.warning(f'No active login activity found for user: {request.user.username}')
#                     except Exception as e:
#                         logger.error(f'Error updating logout time for user: {request.user.username}, error: {e}')

#                 elif curriculum_pattern.match(request.path):
#                     match = curriculum_pattern.match(request.path)
#                     lesson_name = match.group('lesson_name') if match else None

#                     if lesson_name:
#                         if last_activity:
#                             time_spent = current_time - last_activity
#                         else:
#                             time_spent = timedelta(seconds=0)
                        
#                         UserActivity1.objects.create(
#                             user=request.user,
#                             date=current_time,
#                             page_visited=lesson_name,
#                             curriculum_time_spent=time_spent
#                         )
#                     else:
#                         logger.info(f'Non-lesson page visited: {request.path}')
                        
#                 # Record specific activity types
#                 elif video_pattern.match(request.path):
#                     match = video_pattern.match(request.path)
#                     lesson_name = match.group('lesson_name') if match else None

#                     if lesson_name:
#                         time_spent = current_time - last_activity if last_activity else timedelta(seconds=0)
#                         UserActivity1.objects.create(
#                             user=request.user,
#                             date=current_time,
#                             page_visited=lesson_name,
#                             video_time_spent=time_spent
#                         )

#                 elif content_pattern.match(request.path):
#                     match = content_pattern.match(request.path)
#                     lesson_name = match.group('lesson_name') if match else None

#                     if lesson_name:
#                         time_spent = current_time - last_activity if last_activity else timedelta(seconds=0)
#                         UserActivity1.objects.create(
#                             user=request.user,
#                             date=current_time,
#                             page_visited=lesson_name,
#                             content_time_spent=time_spent
#                         )

#                 elif quiz_pattern.match(request.path):
#                     match = quiz_pattern.match(request.path)
#                     lesson_name = match.group('lesson_name') if match else None

#                     if lesson_name:
#                         time_spent = current_time - last_activity if last_activity else timedelta(seconds=0)
#                         UserActivity1.objects.create(
#                             user=request.user,
#                             date=current_time,
#                             page_visited=lesson_name,
#                             quiz_time_spent=time_spent
#                         )

#                 request.session['last_activity'] = current_time.isoformat()
#                 request.session['last_page_visited'] = request.path

#             except Exception as e:
#                 logger.error(f'Error recording activity for user: {request.user.username}, error: {e}')

#         return response