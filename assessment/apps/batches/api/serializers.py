import json
from rest_framework import serializers
from apps.batches.models import Object, Batch


class ObjectSerializer(serializers.ModelSerializer):
    # below is a little hacky to get around the fact that the batch_id is not
    # passed in the /api/v1/batches POST request. I would have preferred to
    # create a separate serializer for the POST request, but I ran out of time.
    batch_id = serializers.CharField(write_only=True, required=False)

    class Meta:
        model = Object
        fields = 'batch_id', 'object_id', 'data',

    def create(self, validated_data):
        try:
            batch_id = validated_data.pop('batch_id', None)
            batch = Batch.objects.get(batch_id=batch_id)
        except Batch.DoesNotExist:
            raise serializers.ValidationError('Batch does not exist')
        validated_data['batch'] = batch

        return Object.objects.create(**validated_data)


class BatchSerializer(serializers.ModelSerializer):
    objects = ObjectSerializer(many=True, source='object_set')

    class Meta:
        model = Batch
        fields = 'batch_id', 'objects',

    def create(self, validated_data):
        objects_data = validated_data.pop('object_set')
        try:
            batch = Batch.objects.get(batch_id=validated_data['batch_id'])
        except Batch.DoesNotExist:
            batch = Batch.objects.create(**validated_data)

        objects_list = [
            Object(batch=batch, **object_data)
            for object_data in objects_data
        ]
        Object.objects.bulk_create(objs=objects_list)
        return batch
