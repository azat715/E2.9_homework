from django.db import models
from django.conf import settings

from core.helper import EmailMsg

# Create your models here.


class EmailStatus(models.IntegerChoices):
    """Статус email Helper"""

    DELIVERING = 0, "delivering"
    DELIVERED = 1, "delivered"
    ERROR = 3, "error"


class EmailSend(models.Model):
    """EmailSend db model"""

    subject = models.CharField(max_length=78)
    message = models.TextField(max_length=255)
    email_from = models.EmailField(default=settings.DEFAULT_FROM_EMAIL)
    timeout = models.PositiveSmallIntegerField()
    status = models.SmallIntegerField(choices=EmailStatus.choices, default=0)

    @classmethod
    def create(cls, obj: EmailMsg):
        instance = cls(subject=obj.subject, message=obj.message, timeout=obj.timeout)
        instance.save()
        return instance

    def get_email_obj(self):
        return EmailMsg(
            self.subject,
            self.message,
            [i["email"] for i in self.email_to.values()],
            self.timeout,
        )


class EmailRecipients(models.Model):
    """EmailRecipients db model
    список email получателей"""

    email_send = models.ForeignKey(
        EmailSend, on_delete=models.CASCADE, related_name="email_to"
    )
    email = models.EmailField()

    @classmethod
    def create(cls, obj: EmailMsg, email: EmailSend):
        emails_to = []
        for i in obj.email_to:
            emails_to.append(cls(email_send=email, email=i))
        cls.objects.bulk_create(emails_to)
