from typing import NamedTuple, List


class EmailMsg(NamedTuple):
    """
    Email
    """

    subject: str
    message: str
    email_from: str
    email_to: List[str]
    timeout: int
    fail_silently: bool = False
