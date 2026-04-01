import datetime
from django.db import models
from django.utils import timezone
from django.contrib import admin

class Member(models.Model):
    vandal_number = models.CharField(max_length=16, primary_key=True)
    last_name = models.CharField(max_length=64)
    first_name = models.CharField(max_length=64)

    def __str__(self):
        full_name = f"{self.last_name}, {self.first_name}"
        return full_name

CLOTHING_CHOICES = [
    ('Shako', [
        ('perc_shako', 'Percussion Shako'),
        ('horn_shako', 'Horn Shako'),
    ]),
    ('Top', [
        ('white_jacket', 'White Jacket'),
        ('black_jacket', 'Black Jacket'),
        ('gritman_jacket', 'Gritman Jacket')
    ]),
    ('Bottom', [
        ('skirt', 'Skirt'),
        ('black_pants', 'Black Pants'),
        ('white_pants', 'White Pants')
    ]),
    ('gauntlet', "Gauntlet")
]

class Uniform_Piece(models.Model):
    clothing_id = models.CharField(max_length=16, primary_key=True)
    size = models.CharField(max_length=32)
    clothing_type = models.CharField(
        max_length=32,
        choices=CLOTHING_CHOICES,
    )
    notes = models.CharField(max_length=128)

    def __str__(self):
        return f"{self.clothing_type}"

class Instrument(models.Model):
    instrument_type = models.CharField(max_length=32)
    instrument_id = models.CharField(max_length=32, primary_key=True)
    notes = models.CharField(max_length=128)

    def __str__(self):
        return f"{self.instrument_type}"

class Rents_Uniform(models.Model):
    vandal_number = models.ForeignKey(Member, on_delete=models.CASCADE)
    uniform_id = models.ForeignKey(Uniform_Piece, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.vandal_number}"

    class Meta:
            # This creates a unique constraint on the pair, effectively acting as a composite PK
            constraints = [
                models.UniqueConstraint(fields=['vandal_number', 'uniform_id'], name='unique_uniform_rental')
            ]

class Rents_Instrument(models.Model):
    vandal_number = models.ForeignKey(Member, on_delete=models.CASCADE)
    instrument_id = models.ForeignKey(Instrument, on_delete=models.CASCADE)

    class Meta:
            # This creates a unique constraint on the pair, effectively acting as a composite PK
            constraints = [
                models.UniqueConstraint(fields=['vandal_number', 'instrument_id'], name='unique_instrument_rental')
            ]
