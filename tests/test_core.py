import pytest
from collections import OrderedDict

from core.serializers import EmailSendSerializer
from core.models import EmailSend, EmailRecipients
from core.service import SenderEmail
from core.helper import EmailMsg


@pytest.mark.django_db
def test_fixture_db(content, email_msg):
    email = EmailSend.objects.count()
    assert email == 1
    email = EmailSend.objects.first()
    assert email.subject == "testing"
    print(email.get_email_obj())
    assert email.get_email_obj() == email_msg


@pytest.mark.django_db
def test_serializer(content, email_msg):
    email = EmailSend.objects.first()
    serializer = EmailSendSerializer(email)
    print(serializer.data)
    assert serializer.data == {
        "id": 1,
        "email_to": [OrderedDict([("email", "azat715@gmail.com")])],
        "subject": "testing",
        "message": "my message",
        "email_from": "hiTSJ5V7@protonmail.com",
        "timeout": 1,
        "status": 0,
    }


@pytest.mark.django_db()
def test_thread_send(email_msg):
    for _ in range(5):
        email = EmailSend.create(email_msg)
        EmailRecipients.create(email_msg, email)
        pk = email.pk
        thread = SenderEmail(email_msg, pk)
        # thread.setDaemon(True)
        thread.start()
