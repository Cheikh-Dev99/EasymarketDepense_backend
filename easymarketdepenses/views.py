from django.shortcuts import render
from rest_framework import viewsets
from .models import Depense
from .serializers import DepenseSerializer

class DepenseViewSet(viewsets.ModelViewSet):
    queryset = Depense.objects.all()
    serializer_class = DepenseSerializer
