import os
import traceback

from django.conf import settings
from django.core.mail import EmailMultiAlternatives

import requests
from celery.utils.log import get_task_logger

from celeryconf import app as celery_app
from core.models import Config

logger = get_task_logger(__name__)


@celery_app.task
def send_sms(to, text, sms_config=None):
    if not sms_config:
        sms_config = Config.get_config("sms_config", "autho").meta
    api_url = sms_config.get("api_url", "http://api.sparrowsms.com/v2/sms/")
    credits = sms_config.get("credits") or None
    headers = sms_config.get("headers") or {}
    if credits:
        if credits == 1:
            text = text[:160]
        elif credits == 2:
            text = text[:306]
        elif credits == 3:
            text = text[:459]
    params = {
        "token": sms_config.get("token"),
        "from": sms_config.get("from"),
        "to": to,
        "text": text,
    }
    response = requests.get(api_url, params=params, headers=headers)
    return response


@celery_app.task
def send_email(
    subject,
    message,
    email,
    cc=[],
    bcc=[],
    subtype="text",
    fileobj=None,
    remove_file=True,
    from_email=None,
    html_data=None,
):
    try:
        if not isinstance(email, list):
            email = [email]

        if not from_email:
            from_email = settings.DEFAULT_FROM_EMAIL

        emailmessage = EmailMultiAlternatives(
            subject, message, from_email, email, cc=cc, bcc=bcc
        )

        if subtype == "html":
            emailmessage.content_subtype = "html"

        if html_data:
            emailmessage.attach_alternative(html_data, "text/html")

        if fileobj:
            if not isinstance(fileobj, list):
                fileobj = [fileobj]
            for obj in fileobj:
                fobj = open(obj["filepath"], "rb")
                emailmessage.attach(
                    obj["filename"], fobj.read(), obj.get("mimetype", "")
                )
                if remove_file:
                    os.remove(obj["filepath"])

        emailmessage.send()
    except Exception:
        admin_msg = "Subject: {}\nTo: {}\nFrom: {}\n{}".format(
            subject, email, from_email, traceback.format_exc()
        )
        logger.error(f"Error email enqueue {admin_msg}")
    return True
