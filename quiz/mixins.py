from django.db import models


class ModelWithTextMixin(models.Model):
    class Meta:
        abstract = True

    text = models.CharField(
        max_length=255,
        verbose_name='Text',
        null=True,
        blank=True
    )

    def __str__(self):
        return '{}'.format(self.text)
