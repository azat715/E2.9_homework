from rest_framework import serializers

from core.models import EmailSend, EmailRecipients
from core.helper import EmailMsg


class EmailRecipientsSerializer(serializers.ModelSerializer):
    class Meta:
        model = EmailRecipients
        fields = "__all__"


class EmailSendSerializer(serializers.ModelSerializer):
    email_to = EmailRecipientsSerializer(many=True)

    class Meta:
        model = EmailSend
        fields = "__all__"

    # def to_internal_value(self, data):
    #     return {
    #         "email": EmailMsg(
    #             data.subject, data.message, data.email_from, data.email_to, data.timeout
    #         ),
    #     }

    # def create(self, validated_data):
    #     email = EmailSend.create(validated_data["email"])
    #     EmailRecipients.create(validated_data["email"], email)
    #     return email
