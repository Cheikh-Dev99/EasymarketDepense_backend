from django.shortcuts import render
from rest_framework import viewsets, status
from rest_framework.response import Response
from .models import Depense
from .serializers import DepenseSerializer
import os


class DepenseViewSet(viewsets.ModelViewSet):
    queryset = Depense.objects.all()
    serializer_class = DepenseSerializer

    def create(self, request, *args, **kwargs):
        try:
            print("Données reçues:", request.data)
            print("Files reçus:", request.FILES)

            data = request.data.copy()

            # Si une catégorie personnalisée est fournie
            if 'custom_category' in data:
                data['category'] = 'AUTRE'  # Force la catégorie à AUTRE

            print("Données formatées:", data)

            serializer = self.get_serializer(data=data)
            if serializer.is_valid():
                self.perform_create(serializer)
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            else:
                print("Erreurs de validation:", serializer.errors)
                return Response(
                    {"detail": serializer.errors},
                    status=status.HTTP_400_BAD_REQUEST
                )
        except Exception as e:
            print("Erreur lors de la création:", str(e))
            return Response(
                {"detail": str(e)},
                status=status.HTTP_400_BAD_REQUEST
            )

    def update(self, request, *args, **kwargs):
        try:
            instance = self.get_object()
            
            # Convertir QueryDict en dictionnaire mutable
            mutable_data = request.data.copy()

            # Gestion de la pièce justificative
            if 'piece_justificative' in mutable_data:
                if mutable_data['piece_justificative'] == 'delete':
                    if instance.piece_justificative:
                        instance.piece_justificative.delete()
                    mutable_data.pop('piece_justificative')
                    instance.piece_justificative = None
                    instance.save()

            # Validation de la catégorie
            category = mutable_data.get('category')
            if category not in ['SALAIRE', 'EAU', 'ELECTRICITE', 'LOYER', 'TRANSPORT', 'APPROVISIONNEMENT', 'AUTRE']:
                return Response(
                    {"category": ["Catégorie invalide"]},
                    status=status.HTTP_400_BAD_REQUEST
                )

            serializer = self.get_serializer(instance, data=mutable_data, partial=True)
            if serializer.is_valid():
                self.perform_update(serializer)
                return Response(serializer.data)
            
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        except Exception as e:
            print("Erreur lors de la mise à jour:", str(e))
            return Response(
                {"detail": str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
