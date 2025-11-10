from rest_framework import serializers


class PhoneCheckSerializer(serializers.Serializer):
    phone_number = serializers.CharField(max_length=20)


class PhoneRegisterSerializer(serializers.Serializer):
    phone_number = serializers.CharField(max_length=20)


class PhoneBulkRegisterSerializer(serializers.Serializer):
    phone_numbers = serializers.ListField(
        child=serializers.CharField(max_length=20),
        max_length=1000
    )

    def validate_phone_numbers(self, value):
        if len(value) > 1000:
            raise serializers.ValidationError("Cannot register more than 1000 phone numbers at once")
        return value


class PhoneCheckResponseSerializer(serializers.Serializer):
    exists = serializers.BooleanField()
    phone_number = serializers.CharField()
    registered_at = serializers.DateTimeField(required=False, allow_null=True)


class PhoneRegisterResponseSerializer(serializers.Serializer):
    success = serializers.BooleanField()
    phone_number = serializers.CharField()
    registered_at = serializers.DateTimeField(required=False, allow_null=True)


class PhoneBulkRegisterResponseSerializer(serializers.Serializer):
    success = serializers.IntegerField()
    failed = serializers.IntegerField()
    results = serializers.ListField()
