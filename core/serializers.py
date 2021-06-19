from rest_framework import serializers

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

    def create(self, validated_data):
        email_msg = EmailMsg(
            validated_data["subject"],
            validated_data["message"],
            [i["email"] for i in validated_data["email_to"]],
            validated_data["timeout"],
        )
        email = EmailSend.create(email_msg)
        EmailRecipients.create(email_msg, email)
        return email
