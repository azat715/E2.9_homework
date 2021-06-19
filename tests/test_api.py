import json
import pytest

from django.urls import reverse
from core.serializers import EmailSendSerializer
from core.models import EmailSend


@pytest.mark.django_db
def test_get_emails(api_client, content):
    response = api_client.get(reverse("core:list_emails", current_app="core"))
    queryset = EmailSend.objects.all()
    serializer = EmailSendSerializer(queryset, many=True)
    print(response.data)
    assert response.data == serializer.data
    assert response.status_code == 200


@pytest.mark.django_db
def test_post_email(api_client, content, post_email):
    response = api_client.post(
        reverse("core:post_email", current_app="core"),
        data=json.dumps(post_email),
        content_type="application/json",
    )
    email = EmailSend.objects.last()
    serializer = EmailSendSerializer(email)
    print(response.data)
    assert response.status_code == 201
    assert response.data == serializer.data
