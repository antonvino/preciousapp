from django.db import models

class TimestampsMixin(models.Model):
    """
    `created_at` and `updated_at`
    """
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Date")
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True