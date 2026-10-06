from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.validators import MinValueValidator, MaxValueValidator


class Usuario(AbstractUser):
    mic = models.BooleanField(default=False)

    gt_xbox = models.CharField(max_length=100, blank=True, null=True)
    steam = models.CharField(max_length=100, blank=True, null=True)
    psn = models.CharField(max_length=100, blank=True, null=True)
    plutonium = models.CharField(max_length=100, blank=True, null=True)

    def __str__(self):
        return self.username


class Juego(models.Model):
    id_juego = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=100)

    def __str__(self):
        return self.nombre


class Mapa(models.Model):
    id_mapa = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=100)

    juego = models.ForeignKey(
        Juego,
        on_delete=models.CASCADE,
        related_name='mapas'
    )

    easter_egg = models.BooleanField(default=False)

    min_ee = models.IntegerField(
        default=1,
        validators=[
            MinValueValidator(1),
            MaxValueValidator(4)
        ]
    )

    dificultad = models.IntegerField(default=1)

    def __str__(self):
        return self.nombre


class Lobby(models.Model):
    id_lobby = models.AutoField(primary_key=True)
    nombre_lobby = models.CharField(max_length=150)

    lider = models.ForeignKey(
        Usuario,
        on_delete=models.CASCADE,
        related_name='lobbies'
    )

    mapa = models.ForeignKey(
        Mapa,
        on_delete=models.CASCADE,
        related_name='lobbies'
    )

    ee = models.BooleanField(default=False)
    free_slots = models.IntegerField(default=3)

    def __str__(self):
        return self.nombre_lobby


class PasoEE(models.Model):
    id_paso = models.AutoField(primary_key=True)

    mapa = models.ForeignKey(
        Mapa,
        on_delete=models.CASCADE,
        related_name='pasos_ee'
    )

    orden = models.IntegerField()
    descripcion = models.TextField()

    class Meta:
        ordering = ['orden']

    def __str__(self):
        return f"{self.mapa.nombre} - Paso {self.orden}"
