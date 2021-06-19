import threading
import time

from django.core.mail import send_mail
from sender_email import app_logger
from core.models import EmailSend, EmailRecipients, EmailStatus
from core.helper import EmailMsg


logger = app_logger.get_logger(__name__)

lock = threading.RLock()


class SenderEmail(threading.Thread):
    def __init__(self, msg: EmailMsg, pk):
        super().__init__()
        self.msg = msg
        self.timeout = msg.timeout
        self.pk = pk

    def run(self):
        logger.info("Запуск потока")
        logger.info("Задержка %s", self.timeout)
        time.sleep(self.timeout)
        test = send_mail(
            self.msg.subject,
            self.msg.message,
            self.msg.email_from,
            self.msg.email_to,
            self.msg.fail_silently,
        )
        logger.info("Test %s", test)
        with lock:
            email = EmailSend.objects.get(pk=self.pk)
            email.status = EmailStatus.DELIVERED
