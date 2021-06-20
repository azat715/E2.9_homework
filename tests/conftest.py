import pytest
from core.helper import EmailMsg
from core.models import EmailRecipients, EmailSend
from rest_framework.test import APIClient


@pytest.fixture(scope="session", name="email_msg")
def fixture_email_msg():
    return EmailMsg("testing", "my message", ["azat715@gmail.com"], 1)


@pytest.fixture(scope="session", name="content")
def fixture_content(django_db_setup, django_db_blocker, email_msg):
    with django_db_blocker.unblock():
        email = EmailSend.create(email_msg)
        EmailRecipients.create(email_msg, email)


@pytest.fixture(scope="session", name="api_client")
def fixture_api_client():
    return APIClient()


@pytest.fixture(name="post_email")
def fixture_post_email():
    return {
        "subject": "testing",
        "message": "my message",
        "timeout": "00:00:02",
        "email_to": "azat715@gmail.com, azar@gog.com, dfdf@fog.ru",
    }
