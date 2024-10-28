import datetime
import os
import uuid
from datetime import datetime

from django.views.decorators.csrf import csrf_exempt
from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view
from django.shortcuts import get_object_or_404

from core.models import ModuleConfiguration
from settings import settings
from .serializers import InsureeSerializer, InsureePhotoSerializer
from .models import Insuree, InsureePhoto


@csrf_exempt
@api_view(['POST'])
def create_insuree_with_photo(request):

    data = request.data.copy()

    if 'card_issued' not in data:
        data['card_issued'] = False

    serializer = InsureeSerializer(data=data)

    if serializer.is_valid():
        insuree = serializer.save()

        config = ModuleConfiguration.objects.get(module='PIECESJOINTES')

        if config and not config.is_enabled:
            return Response({
                "success": True,
                "message": "L'insertion est bien prise en compte, mais la gestion des pièces jointes est désactivée."
            }, status=status.HTTP_201_CREATED)

        photo_file = request.FILES.get('photo_file')
        if photo_file:
            try:

                photo_folder = datetime.now().strftime('%Y/%m')
                upload_path = os.path.join(settings.INSUREE_PHOTOS_ROOT_PATH, photo_folder)
                os.makedirs(upload_path, exist_ok=True)

                file_extension = os.path.splitext(photo_file.name)[1]
                filename = f"{uuid.uuid4()}{file_extension}"

                file_path = os.path.join(upload_path, filename)

                with open(file_path, 'wb') as destination:
                    for chunk in photo_file.chunks():
                        destination.write(chunk)

                photo_data = {
                    "insuree": insuree.id,
                    "chf_id": data.get("chf_id"),
                    "folder": photo_folder,
                    "filename": filename,
                    "officer_id": 1,
                    "date": data.get("photo_date") or datetime.now().date(),
                    "audit_user_id": data.get("audit_user_id", 1)
                }

                photo_serializer = InsureePhotoSerializer(data=photo_data)
                if photo_serializer.is_valid():
                    photo = photo_serializer.save()
                else:

                    os.remove(file_path)
                    return Response(photo_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

            except Exception as e:
                return Response(
                    {
                        "success": False,
                        "message": f"Erreur lors de l'enregistrement de la photo: {str(e)}"},
                    status=status.HTTP_500_INTERNAL_SERVER_ERROR
                )

        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['DELETE'])
def delete_insuree_photo(request, insuree_id):
    """
    Supprime la photo associée à un assuré.

    Parameters:
        insuree_id (int): L'ID de l'assuré dont on veut supprimer la photo
    """
    try:

        insuree = get_object_or_404(Insuree, id=insuree_id)
        print("suprression photo")

        photo = InsureePhoto.objects.filter(
            insuree_id=insuree_id
        ).first()

        if not photo:
            return Response(
                {
                    "success": False,
                    "message": "Aucune photo trouvée pour cet assuré"},
                status=status.HTTP_404_NOT_FOUND
            )

        file_path = os.path.join(
            settings.INSUREE_PHOTOS_ROOT_PATH,
            photo.folder,
            photo.filename
        )

        if file_path and os.path.exists(file_path):
            try:
                os.remove(file_path)
                photo.delete()
                return Response(
                    {
                        "success": True,
                        "message": "Photo supprimée avec succès"
                    },
                    status=status.HTTP_200_OK
                )
            except OSError as e:
                return Response(
                    {
                        "success": False,
                        "message": f"Erreur lors de la suppression du fichier: {str(e)}"},
                    status=status.HTTP_500_INTERNAL_SERVER_ERROR
                )

    except Exception as e:
        return Response(
            {
                "success": False,
                "message": f"Erreur lors de la suppression: {str(e)}"},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )
