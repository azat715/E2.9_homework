from typing import NamedTuple, List

from django.conf import settings


class EmailMsg(NamedTuple):
    """
    Email
    """

    subject: str
    message: str
    email_to: List[str]
    timeout: int
    email_from: str = settings.DEFAULT_FROM_EMAIL
    fail_silently: bool = False
