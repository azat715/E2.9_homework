import multiprocessing
import time

from django.core.mail import send_mail
from sender_email import app_logger
from core.models import EmailSend, EmailStatus
from core.helper import EmailMsg


logger = app_logger.get_logger(__name__)

lock = multiprocessing.Lock()


class SenderEmail(multiprocessing.Process):
    def __init__(self):
        super().__init__()
        self.queue = multiprocessing.Queue()

    def send(self, msg: EmailMsg, pk):
        timeout = int(msg.timeout)
        task = {"msg": msg, "pk": pk}
        self.queue.put(task, timeout)

    def dispatch(self, task):
        msg = task["msg"]
        pk = task["pk"]
        send_mail(
            msg.subject,
            msg.message,
            msg.email_from,
            msg.email_to,
            msg.fail_silently,
        )

        with lock:
            email = EmailSend.objects.get(pk=pk)
            email.status = EmailStatus.DELIVERED
            email.save()

    def run(self):
        while True:
            logger.info("Запуск потока")
            task = self.queue.get()
            self.dispatch(task)
