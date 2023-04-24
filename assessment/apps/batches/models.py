import uuid
import hashlib

from django.db import models
from django.core.exceptions import ValidationError

from apps.core.models import CoreModel
from jsonschema import validate


class Batch(CoreModel):
    batch_id = models.CharField(
        max_length=255,
        default=hashlib.sha1(uuid.uuid4().bytes).hexdigest(),
        unique=True,
    )

    def __str__(self):
        return f'{self.batch_id}'

    class Meta:
        verbose_name_plural = 'Batches'


# Create your models here.
class Object(CoreModel):
    object_id = models.CharField(
        max_length=255,
        default=hashlib.sha1(uuid.uuid4().bytes).hexdigest(),
        unique=True,
    )
    batch = models.ForeignKey(
        to=Batch,
        on_delete=models.PROTECT,
    )
    data = models.JSONField(default=list, blank=True, null=True)

    def __str__(self):
        return f'{self.object_id}'

    def clean(self):
        schema = {
            "$schema": "http://json-schema.org/draft-04/schema#",
            "type": "object",
            "properties": {
                "key": {
                    "type": "string"
                },
                "value": {
                    "type": [
                        "string",
                        "number",
                        "boolean",
                        "null"
                    ]
                }
            },
            "required": [
                "key",
                "value"
            ]
        }
        for item in self.data:
            try:
                validate(instance=item, schema=schema)
            except Exception as e:
                raise ValidationError(f'Invalid data: {e}')

    class Meta:
        verbose_name_plural = 'Objects'
        unique_together = ('object_id', 'batch')
