from rest_framework import serializers
from datetime import time, timedelta

from core.models import EmailSend, EmailRecipients
from core.helper import EmailMsg


class EmailRecipientsSerializer(serializers.ModelSerializer):
    class Meta:
        model = EmailRecipients
        exclude = ["id", "email_send"]


class EmailSendSerializer(serializers.ModelSerializer):
    email_to = EmailRecipientsSerializer(many=True)

    class Meta:
        model = EmailSend
        fields = "__all__"
        read_only_fields = ["status", "email_from"]

    def to_internal_value(self, data):
        # добавить валидацию
        dt = time.fromisoformat(data.get("timeout"))
        data["timeout"] = timedelta(
            hours=dt.hour, minutes=dt.minute, seconds=dt.second
        ).total_seconds()
        email_to = data.get("email_to")
        data["email_to"] = [i for i in email_to.split(",")]
        return data

    def create(self, validated_data):
        email_msg = EmailMsg(
            validated_data["subject"],
            validated_data["message"],
            [i for i in validated_data["email_to"]],
            validated_data["timeout"],
        )
        email = EmailSend.create(email_msg)
        EmailRecipients.create(email_msg, email)
        return email
