import uuid

from django.db import models


class CoreModel(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    created_at = models.DateTimeField(
        auto_created=True,
        auto_now_add=True,
        db_index=True,
    )
    modified_at = models.DateTimeField(
        auto_created=True,
        auto_now=True,
        db_index=True,
        verbose_name='last modified at',
    )

    class Meta:
        abstract = True

    def is_new(self):
        return self._state.adding
