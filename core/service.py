import multiprocessing
import time

from django.core.mail import send_mail
from sender_email import app_logger
from core.models import EmailSend, EmailStatus
from core.helper import EmailMsg


logger = app_logger.get_logger(__name__)

lock = multiprocessing.Lock()


class SenderEmail(multiprocessing.Process):
    def __init__(self, msg: EmailMsg, pk):
        super().__init__()
        self.msg = msg
        self.timeout = msg.timeout
        self.pk = pk

    def run(self):
        logger.info("Запуск потока")
        time.sleep(self.timeout)
        send_mail(
            self.msg.subject,
            self.msg.message,
            self.msg.email_from,
            self.msg.email_to,
            self.msg.fail_silently,
        )
        with lock:
            email = EmailSend.objects.get(pk=self.pk)
            email.status = EmailStatus.DELIVERED
            email.save()
