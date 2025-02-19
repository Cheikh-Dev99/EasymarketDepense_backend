from django.db import models
from django.core.validators import MinValueValidator
from decimal import Decimal

class Depense(models.Model):
    TYPE_CHOICES = [
        ('SALAIRE', 'SALAIRE'),
        ('EAU', 'EAU'),
        ('ELECTRICITE', 'ELECTRICITE'),
        ('LOYER', 'LOYER'),
        ('TRANSPORT', 'TRANSPORT'),
        ('APPROVISIONNEMENT', 'APPROVISIONNEMENT'),
        ('AUTRE', 'AUTRE'),
    ]

    PAYMENT_CHOICES = [
        ('WAVE', 'WAVE'),
        ('ORANGE_MONEY', 'ORANGE MONEY'),
        ('FREE_MONEY', 'FREE MONEY'),
        ('CASH', 'CASH'),
    ]

    title = models.CharField(max_length=200)
    amount = models.DecimalField(
        max_digits=10, 
        decimal_places=2,
        validators=[MinValueValidator(Decimal('0.01'))],
        error_messages={
            'min_value': 'Le montant doit être supérieur à 0'
        }
    )
    category = models.CharField(max_length=50, choices=TYPE_CHOICES)
    custom_category = models.CharField(max_length=50, null=True, blank=True)
    payment_method = models.CharField(max_length=20, choices=PAYMENT_CHOICES)
    piece_justificative = models.FileField(
        upload_to='pieces_justificatives/',
        null=True,
        blank=True
    )
    timestamp = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-timestamp']

    def __str__(self):
        if self.category == 'AUTRE':
            return f"{self.custom_category} - {self.amount} FCFA"
        return f"{self.category} - {self.amount} FCFA"
