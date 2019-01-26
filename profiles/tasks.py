# from django.core.mail import send_mail
#
# from profiles.models import User
# from profiles.utils.suggestedProjectsUtils import get_suggested_projects
# from projects.serializers.getProjectInfoSerializer import GetSuggestedTranslationProjectSerializer
# from sporthub_core.celery import app
#
#
# @app.task(default_retry_delay=3600)
# def send_mass_suggested_projects_email(self):
#     try:
#         suggested_translation_projects = []
#         users = User.objects.all()
#         for user in users:
#             data = []
#             suggested_translation_queryset = get_suggested_projects(user)
#             for project in suggested_translation_queryset:
#                 suggested_translation_projects.append(GetSuggestedTranslationProjectSerializer(project).data)
#             data['suggested_projects'] = suggested_translation_projects
#             try:
#                 send_mail("پروژه های پیشنهادی", str(data), 'noreply@wishwork.ir', [user.email])
#             except:
#                 pass
#
#     except Exception as exc:
#         self.retry(exc=exc)
#
#
# @app.task()
# def send_mass_mail_async():
#     try:
#         users = User.objects.all()
#         for user in users:
#             send_mail("Welcome", "Some Important Notification", 'noreply@wishwork.ir', [user.email])
#     except:
#         pass
#
#
