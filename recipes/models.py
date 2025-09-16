# Create your models here.
# recipes/models.py

from django.conf import settings
from django.db import models
from django.urls import reverse


class Recipe(models.Model):

    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='recipes'
    )
    title = models.CharField("Titlu", max_length=200)
    description = models.TextField("Descriere")
    date_added_str = models.CharField(
        "Data de adăugare (string)",
        max_length=19,
        help_text="Format acceptat: YYYY-MM-DD HH:MM[:SS] — se salvează ca YYYY-MM-DD HH:MM:SS"
    )
    cook_time = models.CharField("Timp de gătire", max_length=50)

    image = models.ImageField("Poză", upload_to="recipes/", blank=True, null=True)

    #  sortarea după data creării
    created_at = models.DateTimeField("Creat la", auto_now_add=True)

    class Meta:
        ordering = ['title']  # pagina principală (/) în ordine alfabetică
        verbose_name = "rețetă"
        verbose_name_plural = "rețete"

    def __str__(self) -> str:
        return self.title

    def get_absolute_url(self) -> str:
        # /recipe/<int:id>/
        return reverse('recipe_detail', kwargs={'id': self.pk})
