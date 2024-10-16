# import logging
# from django.conf import settings
# from django.template.loader import render_to_string
# from django.core.mail import send_mail


# logger = logging.getLogger(__name__)



# def send_email_with_html_body(subject: str, receivers:list, template:str, context:dict):
#     """ This fondtion help to send a customize email to specific user or set of users."""
#     try:
#         # Ensure receivers is a list
#         if not isinstance(receivers, list):
#             receivers = [receivers]
            
#         message = render_to_string(template, context)

#         send_mail(
#             subject,
#             '',
#             receivers,
#             settings.EMAIL_HOST_USER,
#             fail_silently=False,
#             html_message=message
#         )
#         return True

#     except Exception as e:
#         logger.error(e)

#     return False




