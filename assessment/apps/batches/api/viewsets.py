
from rest_framework import viewsets

from apps.batches.models import Object, Batch
from apps.batches.api.serializers import ObjectSerializer, BatchSerializer
from apps.batches.api.filters import BatchSearchFilter, ObjectSearchFilter


class ObjectEntryViewSet(viewsets.ModelViewSet):
    queryset = Object.objects.filter().order_by('-created_at')
    serializer_class = ObjectSerializer
    lookup_field = 'object_id'
    filter_backends = ObjectSearchFilter,
    search_fields = 'data',


class BatchViewSet(viewsets.ModelViewSet):
    queryset = Batch.objects.filter().order_by('-created_at')
    serializer_class = BatchSerializer
    lookup_field = 'batch_id'
    filter_backends = BatchSearchFilter,
    search_fields = 'data',
