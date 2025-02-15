# Documentation Backend EasyMarket

## 1. Architecture Détaillée

### 1.1 Structure du Projet
```
/EasymarketDepense_backend
├── easymarketdepense_backend/    # Configuration principale
│   ├── settings/
│   │   ├── base.py              # Paramètres de base
│   │   ├── development.py       # Configuration développement
│   │   └── production.py        # Configuration production
│   ├── urls.py                  # URLs principales
│   └── wsgi.py                  # Configuration WSGI
├── easymarketdepenses/          # Application principale
│   ├── models/
│   │   ├── depense.py          # Modèle Depense
│   │   └── __init__.py
│   ├── views/
│   │   ├── depense_views.py    # Vues pour les dépenses
│   │   └── __init__.py
│   ├── serializers/
│   │   ├── depense.py          # Sérialiseurs
│   │   └── __init__.py
│   ├── urls.py                 # Routes API
│   └── utils/                  # Utilitaires
├── media/                      # Fichiers uploadés
│   └── pieces_justificatives/
└── requirements/
    ├── base.txt               # Dépendances de base
    ├── development.txt        # Dépendances dev
    └── production.txt         # Dépendances prod
```

### 1.2 Configuration Django Détaillée
```python
# settings/base.py
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'rest_framework',
    'corsheaders',
    'easymarketdepenses',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

# Configuration REST Framework
REST_FRAMEWORK = {
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.PageNumberPagination',
    'PAGE_SIZE': 10,
    'DEFAULT_PARSER_CLASSES': [
        'rest_framework.parsers.JSONParser',
        'rest_framework.parsers.MultiPartParser',
        'rest_framework.parsers.FormParser',
    ],
    'DEFAULT_RENDERER_CLASSES': [
        'rest_framework.renderers.JSONRenderer',
    ],
    'DEFAULT_THROTTLE_CLASSES': [
        'rest_framework.throttling.AnonRateThrottle',
    ],
    'DEFAULT_THROTTLE_RATES': {
        'anon': '100/day',
    }
}

# Configuration CORS
CORS_ALLOWED_ORIGINS = [
    "http://localhost:19006",
    "http://localhost:19000",
    "exp://localhost:19000"
]

CORS_ALLOW_METHODS = [
    'DELETE',
    'GET',
    'OPTIONS',
    'PATCH',
    'POST',
    'PUT',
]

## 2. Modèles de Données

### 2.1 Modèle Depense Détaillé
```python
# models/depense.py
from django.db import models
from django.core.validators import MinValueValidator
from django.core.exceptions import ValidationError
import os

def validate_file_extension(value):
    ext = os.path.splitext(value.name)[1]
    valid_extensions = ['.pdf', '.jpg', '.jpeg', '.png']
    if not ext.lower() in valid_extensions:
        raise ValidationError('Format de fichier non supporté.')

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

    title = models.CharField(
        max_length=200,
        verbose_name="Titre",
        help_text="Titre de la dépense"
    )
    
    amount = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        validators=[MinValueValidator(0)],
        verbose_name="Montant",
        help_text="Montant de la dépense en FCFA"
    )
    
    category = models.CharField(
        max_length=50,
        choices=TYPE_CHOICES,
        verbose_name="Catégorie",
        help_text="Type de dépense"
    )
    
    custom_category = models.CharField(
        max_length=50,
        null=True,
        blank=True,
        verbose_name="Catégorie personnalisée",
        help_text="Requis si la catégorie est 'AUTRE'"
    )
    
    payment_method = models.CharField(
        max_length=20,
        choices=PAYMENT_CHOICES,
        verbose_name="Moyen de paiement"
    )
    
    piece_justificative = models.FileField(
        upload_to='pieces_justificatives/',
        validators=[validate_file_extension],
        null=True,
        blank=True,
        verbose_name="Pièce justificative",
        help_text="PDF ou image (max 5MB)"
    )
    
    timestamp = models.DateTimeField(
        auto_now_add=True,
        verbose_name="Date de création"
    )
    
    updated_at = models.DateTimeField(
        auto_now=True,
        verbose_name="Dernière modification"
    )

    class Meta:
        ordering = ['-timestamp']
        verbose_name = "Dépense"
        verbose_name_plural = "Dépenses"

    def __str__(self):
        return f"{self.title} - {self.amount} FCFA"

    def clean(self):
        if self.category == 'AUTRE' and not self.custom_category:
            raise ValidationError({
                'custom_category': 'Ce champ est requis pour la catégorie AUTRE'
            })

    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)

    @property
    def file_url(self):
        if self.piece_justificative:
            return self.piece_justificative.url
        return None
```

## 3. Sérialiseurs

### 3.1 Sérialiseur Principal
```python
# serializers/depense.py
from rest_framework import serializers
from ..models import Depense

class DepenseSerializer(serializers.ModelSerializer):
    file_url = serializers.SerializerMethodField()
    
    class Meta:
        model = Depense
        fields = [
            'id', 'title', 'amount', 'category',
            'custom_category', 'payment_method',
            'piece_justificative', 'file_url',
            'timestamp', 'updated_at'
        ]
        read_only_fields = ['id', 'timestamp', 'updated_at', 'file_url']

    def get_file_url(self, obj):
        if obj.piece_justificative:
            request = self.context.get('request')
            return request.build_absolute_uri(obj.piece_justificative.url)
        return None

    def validate(self, data):
        """
        Validation personnalisée pour les dépenses
        """
        # Validation de la catégorie personnalisée
        if data.get('category') == 'AUTRE':
            if not data.get('custom_category'):
                raise serializers.ValidationError({
                    'custom_category': 'Ce champ est requis pour la catégorie AUTRE'
                })

        # Validation du montant
        try:
            amount = float(str(data.get('amount')).replace(" ", ""))
            if amount <= 0:
                raise serializers.ValidationError({
                    'amount': 'Le montant doit être supérieur à 0'
                })
        except (ValueError, TypeError):
            raise serializers.ValidationError({
                'amount': 'Format de montant invalide'
            })

        return data

    def validate_piece_justificative(self, value):
        """
        Validation spécifique pour les pièces justificatives
        """
        if value:
            # Vérification de la taille du fichier (max 5MB)
            if value.size > 5 * 1024 * 1024:
                raise serializers.ValidationError(
                    'Le fichier ne doit pas dépasser 5MB'
                )

            # Vérification du type de fichier
            allowed_types = ['image/jpeg', 'image/png', 'application/pdf']
            if hasattr(value, 'content_type') and \
               value.content_type not in allowed_types:
                raise serializers.ValidationError(
                    'Seuls les fichiers JPEG, PNG et PDF sont acceptés'
                )

        return value
```

## 4. Vues et Endpoints

### 4.1 ViewSet Principal
```python
# views/depense_views.py
from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.decorators import action
from django.db.models import Sum
from datetime import datetime, timedelta
from ..models import Depense
from ..serializers import DepenseSerializer

class DepenseViewSet(viewsets.ModelViewSet):
    queryset = Depense.objects.all()
    serializer_class = DepenseSerializer
    
    def get_queryset(self):
        """
        Filtrage personnalisé du queryset
        """
        queryset = Depense.objects.all()
        
        # Filtrage par catégorie
        category = self.request.query_params.get('category', None)
        if category:
            queryset = queryset.filter(category=category)
            
        # Filtrage par moyen de paiement
        payment_method = self.request.query_params.get('payment_method', None)
        if payment_method:
            queryset = queryset.filter(payment_method=payment_method)
            
        # Filtrage par date
        date_from = self.request.query_params.get('date_from', None)
        date_to = self.request.query_params.get('date_to', None)
        if date_from and date_to:
            try:
                date_from = datetime.strptime(date_from, '%Y-%m-%d')
                date_to = datetime.strptime(date_to, '%Y-%m-%d')
                queryset = queryset.filter(
                    timestamp__date__range=[date_from, date_to]
                )
            except ValueError:
                pass
                
        # Recherche textuelle
        search = self.request.query_params.get('search', None)
        if search:
            queryset = queryset.filter(title__icontains=search)
            
        # Tri
        ordering = self.request.query_params.get('ordering', '-timestamp')
        return queryset.order_by(ordering)

    def perform_create(self, serializer):
        """
        Création d'une dépense avec gestion des fichiers
        """
        try:
            serializer.save()
        except Exception as e:
            # Nettoyage des fichiers en cas d'erreur
            if 'piece_justificative' in serializer.validated_data:
                file = serializer.validated_data['piece_justificative']
                if hasattr(file, 'temporary_file_path'):
                    os.remove(file.temporary_file_path())
            raise e

    @action(detail=False, methods=['get'])
    def statistics(self, request):
        """
        Endpoint pour les statistiques des dépenses
        """
        # Calcul des totaux par catégorie
        category_totals = self.get_queryset().values('category')\
            .annotate(total=Sum('amount'))
            
        # Calcul des totaux par moyen de paiement
        payment_totals = self.get_queryset().values('payment_method')\
            .annotate(total=Sum('amount'))
            
        # Calcul des totaux par période
        today = datetime.now()
        month_start = today.replace(day=1, hour=0, minute=0, second=0)
        
        monthly_total = self.get_queryset()\
            .filter(timestamp__gte=month_start)\
            .aggregate(total=Sum('amount'))

        return Response({
            'category_totals': category_totals,
            'payment_totals': payment_totals,
            'monthly_total': monthly_total['total'] or 0
        })

    def destroy(self, request, *args, **kwargs):
        """
        Suppression d'une dépense avec nettoyage des fichiers
        """
        instance = self.get_object()
        
        # Suppression du fichier associé
        if instance.piece_justificative:
            file_path = instance.piece_justificative.path
            if os.path.exists(file_path):
                os.remove(file_path)
                
        return super().destroy(request, *args, **kwargs)
```

## 5. Gestion des Fichiers

### 5.1 Configuration du Stockage
```python
# settings/base.py
import os

# Configuration locale
MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

# Configuration S3 pour production
if not DEBUG:
    AWS_ACCESS_KEY_ID = os.environ.get('AWS_ACCESS_KEY_ID')
    AWS_SECRET_ACCESS_KEY = os.environ.get('AWS_SECRET_ACCESS_KEY')
    AWS_STORAGE_BUCKET_NAME = os.environ.get('AWS_STORAGE_BUCKET_NAME')
    AWS_S3_REGION_NAME = 'us-east-1'
    AWS_DEFAULT_ACL = None
    AWS_S3_SIGNATURE_VERSION = 's3v4'
    
    # Configuration du stockage S3
    DEFAULT_FILE_STORAGE = 'storages.backends.s3boto3.S3Boto3Storage'
    STATICFILES_STORAGE = 'storages.backends.s3boto3.S3Boto3Storage'
```

### 5.2 Gestionnaire de Fichiers Personnalisé
```python
# utils/file_handlers.py
import os
import uuid
from django.core.files.storage import default_storage
from django.core.files.base import ContentFile
from PIL import Image
from io import BytesIO

class FileHandler:
    @staticmethod
    def handle_uploaded_file(file, max_size_mb=5):
        """Gère le traitement des fichiers uploadés"""
        
        # Vérification de la taille
        if file.size > max_size_mb * 1024 * 1024:
            raise ValueError(f"Le fichier dépasse {max_size_mb}MB")

        # Génération d'un nom unique
        ext = os.path.splitext(file.name)[1]
        unique_filename = f"{uuid.uuid4()}{ext}"

        # Traitement selon le type de fichier
        if file.content_type.startswith('image/'):
            return FileHandler.process_image(file, unique_filename)
        elif file.content_type == 'application/pdf':
            return FileHandler.process_pdf(file, unique_filename)
        else:
            raise ValueError("Type de fichier non supporté")

    @staticmethod
    def process_image(image_file, filename):
        """Traite et optimise les images"""
        try:
            # Ouverture de l'image
            img = Image.open(image_file)
            
            # Conversion en RGB si nécessaire
            if img.mode != 'RGB':
                img = img.convert('RGB')

            # Redimensionnement si trop grande
            max_size = (1920, 1080)
            if img.size[0] > max_size[0] or img.size[1] > max_size[1]:
                img.thumbnail(max_size, Image.LANCZOS)

            # Compression
            output = BytesIO()
            img.save(output, format='JPEG', quality=85, optimize=True)
            output.seek(0)

            # Sauvegarde
            path = f'pieces_justificatives/{filename}'
            saved_path = default_storage.save(path, ContentFile(output.read()))
            
            return saved_path

        except Exception as e:
            raise ValueError(f"Erreur lors du traitement de l'image: {str(e)}")

    @staticmethod
    def process_pdf(pdf_file, filename):
        """Traite les fichiers PDF"""
        try:
            path = f'pieces_justificatives/{filename}'
            saved_path = default_storage.save(path, pdf_file)
            return saved_path
            
        except Exception as e:
            raise ValueError(f"Erreur lors du traitement du PDF: {str(e)}")
```

## 6. Sécurité

### 6.1 Configuration de Sécurité
```python
# settings/production.py
# Paramètres de sécurité
SECURE_SSL_REDIRECT = True
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True
SECURE_BROWSER_XSS_FILTER = True
SECURE_CONTENT_TYPE_NOSNIFF = True
X_FRAME_OPTIONS = 'DENY'

# Protection contre les attaques CSRF
CSRF_TRUSTED_ORIGINS = [
    'https://easymarketdepense-backend.onrender.com'
]

# Paramètres de mot de passe
AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
        'OPTIONS': {
            'min_length': 9,
        }
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]

# Configuration du rate limiting
REST_FRAMEWORK['DEFAULT_THROTTLE_CLASSES'] = [
    'rest_framework.throttling.AnonRateThrottle',
    'rest_framework.throttling.UserRateThrottle'
]

REST_FRAMEWORK['DEFAULT_THROTTLE_RATES'] = {
    'anon': '100/day',
    'user': '1000/day'
}
```

### 6.2 Middleware de Sécurité
```python
# middleware.py
import re
from django.http import HttpResponseForbidden

class SecurityMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
        # Compilation des expressions régulières pour les attaques courantes
        self.xss_pattern = re.compile(r'<script.*?>.*?</script>', re.I)
        self.sql_pattern = re.compile(
            r'(\bSELECT\b|\bUNION\b|\bINSERT\b|\bDROP\b|\bDELETE\b|\bUPDATE\b)',
            re.I
        )

    def __call__(self, request):
        # Vérification des paramètres de requête
        for key, value in request.GET.items():
            if self._check_malicious_content(value):
                return HttpResponseForbidden("Contenu malveillant détecté")

        # Vérification du corps de la requête
        if request.method in ['POST', 'PUT', 'PATCH']:
            if hasattr(request, 'body'):
                body_str = request.body.decode('utf-8', errors='ignore')
                if self._check_malicious_content(body_str):
                    return HttpResponseForbidden("Contenu malveillant détecté")

        response = self.get_response(request)
        return response

    def _check_malicious_content(self, content):
        """Vérifie la présence de contenu malveillant"""
        if isinstance(content, str):
            # Vérification XSS
            if self.xss_pattern.search(content):
                return True
            # Vérification injection SQL
            if self.sql_pattern.search(content):
                return True
        return False
```

## 7. Déploiement

### 7.1 Configuration Render
```yaml
# render.yaml
services:
  - type: web
    name: easymarketdepense-backend
    env: python
    buildCommand: |
      python -m pip install --upgrade pip
      pip install -r requirements/production.txt
      python manage.py collectstatic --noinput
      python manage.py migrate
    startCommand: gunicorn easymarketdepense_backend.wsgi:application
    envVars:
      - key: PYTHON_VERSION
        value: 3.9.0
      - key: DATABASE_URL
        fromDatabase:
          name: easymarketdepense_db
          property: connectionString
      - key: SECRET_KEY
        generateValue: true
      - key: DJANGO_SETTINGS_MODULE
        value: easymarketdepense_backend.settings.production
      - key: AWS_ACCESS_KEY_ID
        sync: false
      - key: AWS_SECRET_ACCESS_KEY
        sync: false
      - key: AWS_STORAGE_BUCKET_NAME
        value: easymarketdepense-files

databases:
  - name: easymarketdepense_db
    databaseName: easymarketdepense
    user: easymarketdepense
    plan: starter
```

### 7.2 Configuration Gunicorn
```python
# gunicorn.conf.py
import multiprocessing

# Configuration des workers
workers = multiprocessing.cpu_count() * 2 + 1
threads = 2
worker_class = 'gthread'
worker_connections = 1000

# Timeouts
timeout = 120
keepalive = 5

# Logging
accesslog = '-'
errorlog = '-'
loglevel = 'info'

# Configuration SSL
keyfile = None
certfile = None

# Configuration des en-têtes
forwarded_allow_ips = '*'
proxy_protocol = True
proxy_allow_ips = '*'

def on_starting(server):
    """Log when server starts"""
    server.log.info("Starting Gunicorn Server")

def on_exit(server):
    """Log when server exits"""
    server.log.info("Stopping Gunicorn Server")

def worker_abort(worker):
    """Log worker crashes"""
    worker.log.warning(f"Worker {worker.pid} crashed")
```

## 8. Monitoring et Logging

### 8.1 Configuration des Logs
```python
# settings/production.py
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'verbose': {
            'format': '{levelname} {asctime} {module} {process:d} {thread:d} {message}',
            'style': '{',
        },
        'simple': {
            'format': '{levelname} {message}',
            'style': '{',
        },
    },
    'filters': {
        'require_debug_false': {
            '()': 'django.utils.log.RequireDebugFalse',
        },
        'require_debug_true': {
            '()': 'django.utils.log.RequireDebugTrue',
        },
    },
    'handlers': {
        'console': {
            'level': 'INFO',
            'filters': ['require_debug_true'],
            'class': 'logging.StreamHandler',
            'formatter': 'simple'
        },
        'file': {
            'level': 'ERROR',
            'class': 'logging.FileHandler',
            'filename': 'django-errors.log',
            'formatter': 'verbose'
        },
        'mail_admins': {
            'level': 'ERROR',
            'filters': ['require_debug_false'],
            'class': 'django.utils.log.AdminEmailHandler'
        }
    },
    'loggers': {
        'django': {
            'handlers': ['console', 'file'],
            'level': 'INFO',
            'propagate': True,
        },
        'django.request': {
            'handlers': ['mail_admins', 'file'],
            'level': 'ERROR',
            'propagate': False,
        },
        'easymarketdepenses': {
            'handlers': ['console', 'file'],
            'level': 'INFO',
            'propagate': True,
        }
    }
}
```

### 8.2 Middleware de Performance
```python
# middleware.py
import time
import logging
from django.db import connection
from django.conf import settings

logger = logging.getLogger('easymarketdepenses')

class PerformanceMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Temps de début
        start_time = time.time()

        # Nombre de requêtes DB au début
        n_queries_start = len(connection.queries)

        response = self.get_response(request)

        # Calcul du temps d'exécution
        duration = time.time() - start_time

        # Calcul du nombre de requêtes DB
        n_queries = len(connection.queries) - n_queries_start

        # Log si la requête est lente
        if duration > 1.0:  # Plus d'une seconde
            logger.warning(
                f'Slow request: {request.path} took {duration:.2f}s '
                f'with {n_queries} queries'
            )

        # Ajout des en-têtes de performance
        response['X-Page-Generation-Duration-ms'] = int(duration * 1000)
        response['X-Queries-Count'] = n_queries

        return response
```

### 8.3 Monitoring des Requêtes SQL
```python
# utils/sql_monitoring.py
from django.db import connection
from functools import wraps
import logging
import time

logger = logging.getLogger('easymarketdepenses')

def log_sql_queries(func):
    """Décorateur pour logger les requêtes SQL"""
    @wraps(func)
    def wrapper(*args, **kwargs):
        queries_start = len(connection.queries)
        
        start = time.time()
        result = func(*args, **kwargs)
        duration = time.time() - start
        
        queries_end = len(connection.queries)
        queries_executed = connection.queries[queries_start:queries_end]
        
        if queries_executed:
            logger.info(f"""
                Function: {func.__name__}
                Number of queries: {len(queries_executed)}
                Execution time: {duration:.2f}s
                Queries:
                {'-' * 80}
                {'\n'.join(query['sql'] for query in queries_executed)}
                {'-' * 80}
            """)
            
        return result
    return wrapper
```

## 9. Tests

### 9.1 Tests Unitaires
```python
# tests/test_models.py
from django.test import TestCase
from django.core.exceptions import ValidationError
from decimal import Decimal
from ..models import Depense

class DepenseModelTests(TestCase):
    def setUp(self):
        self.depense_data = {
            'title': 'Test Dépense',
            'amount': Decimal('1000.00'),
            'category': 'SALAIRE',
            'payment_method': 'WAVE'
        }

    def test_create_depense(self):
        depense = Depense.objects.create(**self.depense_data)
        self.assertEqual(depense.title, 'Test Dépense')
        self.assertEqual(depense.amount, Decimal('1000.00'))

    def test_invalid_amount(self):
        self.depense_data['amount'] = Decimal('-100.00')
        with self.assertRaises(ValidationError):
            Depense.objects.create(**self.depense_data)

    def test_custom_category_required(self):
        self.depense_data['category'] = 'AUTRE'
        with self.assertRaises(ValidationError):
            Depense.objects.create(**self.depense_data)
```

### 9.2 Tests d'Intégration API
```python
# tests/test_api.py
from rest_framework.test import APITestCase
from rest_framework import status
from django.urls import reverse
from django.core.files.uploadedfile import SimpleUploadedFile
import json

class DepenseAPITests(APITestCase):
    def setUp(self):
        self.url = reverse('depense-list')
        self.depense_data = {
            'title': 'Test API',
            'amount': '1000.00',
            'category': 'SALAIRE',
            'payment_method': 'WAVE'
        }

    def test_create_depense(self):
        response = self.client.post(
            self.url,
            self.depense_data,
            format='json'
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['title'], 'Test API')

    def test_file_upload(self):
        # Création d'un fichier test
        file_content = b'test file content'
        test_file = SimpleUploadedFile(
            "test.pdf",
            file_content,
            content_type="application/pdf"
        )

        # Ajout du fichier aux données
        data = self.depense_data.copy()
        data['piece_justificative'] = test_file

        response = self.client.post(
            self.url,
            data,
            format='multipart'
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertIsNotNone(response.data['file_url'])

    def test_filter_depenses(self):
        # Création de dépenses test
        self.client.post(self.url, self.depense_data, format='json')
        
        # Test du filtrage
        response = self.client.get(
            f"{self.url}?category=SALAIRE"
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 1)
```