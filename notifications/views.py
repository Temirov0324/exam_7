from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from django.utils.translation import gettext_lazy as _
from .models import Notification
from .serializers import NotificationSerializer

class NotificationListView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        notifications = Notification.objects.filter(recipient=request.user)
        serializer = NotificationSerializer(notifications, many=True, context={'request': request})
        return Response(serializer.data)

class NotificationDetailView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, pk):
        try:
            notification = Notification.objects.get(pk=pk)
            if notification.recipient != request.user:
                return Response({"error": _("Bu xabarnoma sizga tegishli emas")}, status=status.HTTP_403_FORBIDDEN)
            serializer = NotificationSerializer(notification, context={'request': request})
            return Response(serializer.data)
        except Notification.DoesNotExist:
            return Response({"error": _("Xabarnoma topilmadi")}, status=status.HTTP_404_NOT_FOUND)

    def put(self, request, pk):
        try:
            notification = Notification.objects.get(pk=pk)
            if notification.recipient != request.user:
                return Response({"error": _("Siz bu xabarnomani o‘zgartira olmaysiz")}, status=status.HTTP_403_FORBIDDEN)
            serializer = NotificationSerializer(notification, data=request.data, partial=True, context={'request': request})
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Notification.DoesNotExist:
            return Response({"error": _("Xabarnoma topilmadi")}, status=status.HTTP_404_NOT_FOUND)

    def delete(self, request, pk):
        try:
            notification = Notification.objects.get(pk=pk)
            if notification.recipient != request.user:
                return Response({"error": _("Siz bu xabarnomani o‘chira olmaysiz")}, status=status.HTTP_403_FORBIDDEN)
            notification.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        except Notification.DoesNotExist:
            return Response({"error": _("Xabarnoma topilmadi")}, status=status.HTTP_404_NOT_FOUND)