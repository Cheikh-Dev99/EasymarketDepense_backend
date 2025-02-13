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
        instance = self.get_object()
        piece_justificative = request.data.get('piece_justificative')

        if piece_justificative == 'delete':
            if instance.piece_justificative:
                if os.path.isfile(instance.piece_justificative.path):
                    os.remove(instance.piece_justificative.path)
                instance.piece_justificative = None
                instance.save()
            # Retirer le champ avant l'update
            request.data.pop('piece_justificative', None)

        return super().update(request, *args, **kwargs)
