from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from core.serializers import EmailSendSerializer
from core.models import EmailSend
from core.service import SenderEmail

# Create your views here.
@api_view(["POST"])
def post_email(request):
    serializer = EmailSendSerializer(data=request.data)
    if serializer.is_valid():
        email = serializer.save()
        thread = SenderEmail(email.get_email_obj(), email.pk)
        thread.start()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view()
def list_emails(request):
    queryset = EmailSend.objects.all()
    serializer = EmailSendSerializer(queryset, many=True)
    return Response(serializer.data)
