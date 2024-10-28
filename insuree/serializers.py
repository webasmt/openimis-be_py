from rest_framework import serializers
from .models import Insuree, InsureePhoto


class InsureePhotoSerializer(serializers.ModelSerializer):

    officer_id = serializers.IntegerField(default=1)

    class Meta:
        model = InsureePhoto
        fields = ['chf_id', 'insuree', 'folder', 'filename', 'photo', 'officer_id', 'date']


class InsureeSerializer(serializers.ModelSerializer):

    photo = InsureePhotoSerializer(required=False)
    card_issued = serializers.BooleanField(default=False)
    audit_user_id = serializers.IntegerField(default=1)

    class Meta:
        model = Insuree
        fields = ['chf_id', 'last_name', 'other_names', 'dob', 'head', 'photo', 'card_issued', 'audit_user_id']

    def create(self, validated_data):
        # Extraire les données de la photo
        photo_data = validated_data.pop('photo', None)

        # Créer l'Insuree
        insuree = Insuree.objects.create(**validated_data)

        # Si des données de photo sont fournies, créer l'InsureePhoto associée
        if photo_data:
            photo = InsureePhoto.objects.create(**photo_data)
            insuree.photo = photo
            insuree.save()

        return insuree
