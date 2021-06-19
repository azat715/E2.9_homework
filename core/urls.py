from django.urls import path

from core.views import post_email, list_emails


app_name = "core"

urlpatterns = [
    path("", list_emails, name="list_emails"),
    path("email", post_email, name="post_email"),
]
