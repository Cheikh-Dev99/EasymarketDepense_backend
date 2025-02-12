from django.db import models

class Depense(models.Model):
    TYPE_CHOICES = [
        ('SALAIRE', 'Salaire'),
        ('EAU', 'Eau'),
        ('ELECTRICITE', 'Électricité'),
        ('LOYER', 'Loyer'),
        ('TRANSPORT', 'Transport'),
        ('APPROVISIONNEMENT', 'Approvisionnement Produit'),
        ('AUTRE', 'Autre'),
    ]

    PAYMENT_CHOICES = [
        ('WAVE', 'Wave'),
        ('ORANGE_MONEY', 'Orange Money'),
        ('FREE_MONEY', 'Free Money'),
        ('CASH', 'Cash'),
    ]

    title = models.CharField(max_length=200)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    category = models.CharField(max_length=50, choices=TYPE_CHOICES)
    custom_category = models.CharField(max_length=50, blank=True, null=True)
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
        return f"{self.title} - {self.amount} FCFA"
