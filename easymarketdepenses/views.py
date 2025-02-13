from django.shortcuts import render
from rest_framework import viewsets, status
from rest_framework.response import Response
from .models import Depense
from .serializers import DepenseSerializer


class DepenseViewSet(viewsets.ModelViewSet):
    queryset = Depense.objects.all()
    serializer_class = DepenseSerializer

    def create(self, request, *args, **kwargs):
        try:
            print("Données reçues:", request.data)
            print("Files reçus:", request.FILES)

            # Préparer les données
            data = {
                'title': request.data.get('title'),
                'amount': request.data.get('amount'),
                'category': request.data.get('category'),
                'payment_method': request.data.get('payment_method'),
            }

            # Ajouter la pièce justificative si présente
            if 'piece_justificative' in request.FILES:
                data['piece_justificative'] = request.FILES['piece_justificative']

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
