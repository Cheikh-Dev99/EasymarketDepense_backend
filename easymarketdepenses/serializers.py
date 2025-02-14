from rest_framework import serializers
from .models import Depense


class DepenseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Depense
        fields = '__all__'

    def validate(self, data):
        if data.get('category') == 'AUTRE' and not data.get('custom_category'):
            if not self.instance or not self.instance.custom_category:
                raise serializers.ValidationError(
                    {"custom_category": "Ce champ est requis pour la catégorie 'AUTRE'"}
                )
        return data

    def validate_amount(self, value):
        try:
            cleaned_value = str(value).replace(" ", "")
            float_value = float(cleaned_value)
            if float_value <= 0:
                raise serializers.ValidationError(
                    "Le montant doit être supérieur à 0")
            return cleaned_value
        except ValueError:
            raise serializers.ValidationError(
                "Le montant doit être un nombre valide")
