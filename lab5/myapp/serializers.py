import os
import re
from django.conf import settings
from rest_framework import serializers
from cryptography.hazmat.primitives.ciphers.aead import AESGCM

from myapp.models import SensitiveData, User


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'


class SensitiveDataSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)

    def __init__(self, *args, **kwargs):
        self.aesgcm = AESGCM(settings.AESGCM_KEY)
        super().__init__(*args, **kwargs)

    class Meta:
        model = SensitiveData
        fields = (
            'data',
            'user'
        )
        encrypted_fields = (
            'data',
        )

    def create(self, validated_data):
        encrypted_data = self._encrypt_fields(validated_data)
        return super().create(encrypted_data)

    def update(self, instance, validated_data):
        encrypted_data = self._encrypt_fields(validated_data)
        return super().update(instance, encrypted_data)

    def to_representation(self, data):
        data = super().to_representation(data)
        decrypted_data = self._decrypt_fields(data)
        return decrypted_data

    def _encrypt_fields(self, data):
        field_names = self.Meta.encrypted_fields
        for field in field_names:
            if data.get(field) is None:
                continue
            nonce = os.urandom(12)
            encrypted = self.aesgcm.encrypt(nonce, data[field].encode(), str(self.context['user'].id).encode())
            data[field] = (b"aesgcm:::" + encrypted + b":::" + nonce).decode('raw_unicode_escape')
        return data

    def _decrypt_fields(self, data):
        field_names = self.Meta.encrypted_fields
        encrypted_regex = re.compile("^aesgcm:::(?P<encrypted>.*):::(?P<nonce>.*)$")
        for field in field_names:
            if data.get(field) is None:
                continue
            match = encrypted_regex.match(data[field])
            encrypted = match.group('encrypted').encode('raw_unicode_escape')
            nonce = match.group('nonce').encode('raw_unicode_escape')
            decrypted = self.aesgcm.decrypt(nonce, encrypted, str(self.context['user'].id).encode())
            data[field] = decrypted.decode()
        return data
