from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from asgiref.sync import async_to_sync
from .serializers import (
    PhoneCheckSerializer,
    PhoneRegisterSerializer,
    PhoneBulkRegisterSerializer,
    PhoneCheckResponseSerializer,
    PhoneRegisterResponseSerializer,
    PhoneBulkRegisterResponseSerializer
)
from .services import PhoneRegistryService
import logging

logger = logging.getLogger(__name__)


class PhoneCheckView(APIView):
    """Check if a phone number exists."""

    def post(self, request):
        serializer = PhoneCheckSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        phone_number = serializer.validated_data['phone_number']
        
        try:
            service = PhoneRegistryService()
            result = async_to_sync(service.check_phone)(phone_number)
            return Response(result, status=status.HTTP_200_OK)
        except Exception as e:
            logger.error(f"Error checking phone: {e}")
            return Response(
                {'detail': 'Failed to check phone number'},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


class PhoneRegisterView(APIView):
    """Register a phone number."""

    def post(self, request):
        serializer = PhoneRegisterSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        phone_number = serializer.validated_data['phone_number']
        
        try:
            service = PhoneRegistryService()
            result = async_to_sync(service.register_phone)(phone_number)
            return Response(result, status=status.HTTP_201_CREATED)
        except Exception as e:
            logger.error(f"Error registering phone: {e}")
            return Response(
                {'detail': 'Failed to register phone number'},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


class PhoneBulkRegisterView(APIView):
    """Bulk register phone numbers."""

    def post(self, request):
        serializer = PhoneBulkRegisterSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        phone_numbers = serializer.validated_data['phone_numbers']
        
        try:
            service = PhoneRegistryService()
            result = async_to_sync(service.bulk_register_phones)(phone_numbers)
            return Response(result, status=status.HTTP_200_OK)
        except Exception as e:
            logger.error(f"Error bulk registering phones: {e}")
            return Response(
                {'detail': 'Failed to bulk register phone numbers'},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


class PhoneCleanupView(APIView):
    """Cleanup old phone registry records."""

    def delete(self, request):
        days = request.query_params.get('days', 90)
        
        try:
            days = int(days)
        except ValueError:
            return Response(
                {'detail': 'days must be an integer'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        try:
            service = PhoneRegistryService()
            result = async_to_sync(service.cleanup_old_records)(days)
            return Response(result, status=status.HTTP_200_OK)
        except Exception as e:
            logger.error(f"Error cleaning up phone records: {e}")
            return Response(
                {'detail': 'Failed to cleanup phone records'},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
