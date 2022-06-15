from django.db import models
from django.utils.translation import gettext_lazy as _


class Photo(models.Model):
    image = models.ImageField(upload_to="photos", verbose_name=_("Фото"))
    description = models.CharField(max_length=50, verbose_name=_("Короткий опис / назва"))

    def __str__(self):
        return self.description

    class Meta:
        verbose_name = _("Фотографія")
        verbose_name_plural = _("Фотографії")