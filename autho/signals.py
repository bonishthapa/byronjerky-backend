from django.dispatch import receiver

from decouple import config
from django_rest_passwordreset.signals import reset_password_token_created


@receiver(reset_password_token_created)
def password_reset_token_created(
    sender, instance, reset_password_token, *args, **kwargs
):
    FRONT_END_HOST = config("FRONT_END_HOST", default="http://localhost:8082")
    # print(reset_password_token.key)
    message = f"""To reset password for your {reset_password_token.user.email} Account,
    Click the link below:
    {FRONT_END_HOST}/#/reset-password/{reset_password_token.key}/
    If clicking the link above doesn't work, please copy and paste the URL in a new browser window instead.
    Sincerely,
    Team
    """
    reset_password_token.user.send_email(
        subject="Password Reset",
        message=message,
    )
