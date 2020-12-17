from django.db import models
from django.urls import reverse
from apps.testauth.models import TestUser
import uuid
import secrets


# Create your models here.
class Tenant(models.Model):
    id = models.CharField(max_length=255, default=uuid.uuid4, primary_key=True)
    name = models.CharField(null=False, max_length=255)
    identifier = models.CharField(null=False, max_length=255, default=uuid.uuid4)
    token = models.CharField(null=False, max_length=100, default=secrets.token_urlsafe)

    def corporations(self):
        return Corporation.objects.filter(tenant=self)

    def __str__(self):
        return self.name


class Corporation(models.Model):
    name = models.CharField(null=False, max_length=255)
    corporation_id = models.IntegerField(null=False)
    ceo_id = models.IntegerField(null=False)
    last_pull = models.DateField(null=True)
    process_payments = models.BooleanField(default=False)
    process_taxes = models.BooleanField(default=False)
    tenant = models.ForeignKey(Tenant, on_delete=models.CASCADE, null=True)

    def __str__(self):
        return self.name


class Character(models.Model):
    character_id = models.IntegerField(null=False)
    name = models.CharField(null=False, max_length=255)
    corporation = models.ForeignKey(Corporation, on_delete=models.CASCADE)
    isValid = models.BooleanField(null=False, default=False)
    join_date = models.DateField(null=False)
    start_date = models.DateField(null=True)
    user = models.ForeignKey(TestUser, models.PROTECT)

    def __str__(self):
        return self.name


SOURCE_CHOICES = [
    (60003760, 'Jita'),
    (60008494, 'Amarr'),
    (60011866, 'Dodixie'),
    (60004588, 'Rens'),
    (60005686, 'Hek')
]

SOURCE_TYPE_CHOICES = [
    ('buy', 'Buy Orders'),
    ('sell', 'Sell Orders')
]

SOURCE_STAT_CHOICES = [
    ('weightedAverage', 'Weighted Average'),
    ('max', 'Max Price'),
    ('min', 'Min Price'),
    ('stddev', 'Standard Deviation'),
    ('median', 'Median'),
    ('percentile', 'Percentile')
]

LATE_FEE_DAY_CHOICES = [
    (-1, 'Pick a day...'),
    (1, '1'),
    (2, '2'),
    (3, '3'),
    (4, '4'),
    (5, '5'),
    (6, '6'),
    (7, '7'),
    (8, '8'),
    (9, '9'),
    (10, '10'),
    (11, '11'),
    (12, '12'),
    (13, '13'),
    (14, '14'),
    (15, '15'),
    (30, 'Last Day...'),
]


class Setting(models.Model):
    tenant = models.ForeignKey(Tenant, on_delete=models.CASCADE, null=False)
    start_date = models.DateField(null=True, blank=True)
    mineral_tax_rate = models.IntegerField(null=False, default=5)
    goo_tax_rate = models.IntegerField(null=False, default=5)
    source = models.IntegerField(null=False, default=60003760, choices=SOURCE_CHOICES)
    source_type = models.CharField(null=False, max_length=4, default='buy', choices=SOURCE_TYPE_CHOICES)
    source_stat = models.CharField(null=False, max_length=50, default='percentile', choices=SOURCE_STAT_CHOICES)
    source_modifier = models.IntegerField(null=False, default=90)
    ice_refine_rate = models.FloatField(null=False, default=89.3)
    ore_refine_rate = models.FloatField(null=False, default=89.3)
    moon_refine_rate = models.FloatField(null=False, default=89.3)
    late_fees_enabled = models.BooleanField(null=False, default=False)
    late_fee_threshold = models.IntegerField(null=False, default=0)
    late_fee_day = models.IntegerField(null=False, default=-1, choices=LATE_FEE_DAY_CHOICES)
    late_fee_charge = models.IntegerField(null=False, default=10)

    def __str__(self):
        return f'Settings for {self.tenant.name}'

    def get_absolute_url(self):
        return reverse('tenant_admin', kwargs={'tenant_id': self.tenant_id})
