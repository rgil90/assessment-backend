import json

from rest_framework import filters

from django.db.models import Q


class BatchSearchFilter(filters.BaseFilterBackend):
    def filter_queryset(self, request, queryset, view):
        data_params = request.query_params.get('data', None)
        if data_params is not None:
            try:
                data_dict = json.loads(data_params)

                q_filters = Q()
                for key, value in data_dict.items():
                    q_filters |= Q(object__data__contains=[{'key': f'{key}', 'value': f'{value}'}])

                queryset = queryset.filter(q_filters)

            except ValueError:
                return queryset.none()
        return queryset


class ObjectSearchFilter(filters.BaseFilterBackend):
    def filter_queryset(self, request, queryset, view):
        data_params = request.query_params.get('data', None)
        if data_params is not None:
            try:
                data_dict = json.loads(data_params)
                q_filters = Q()
                for key, value in data_dict.items():
                    q_filters |= Q(data__contains=[{'key': f'{key}', 'value': f'{value}'}])
                queryset = queryset.filter(q_filters)
            except ValueError:
                return queryset.none()
        return queryset
