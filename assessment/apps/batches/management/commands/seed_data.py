from django.core.management.base import BaseCommand
import os
import json
from django.apps import apps


class Command(BaseCommand):
    help = 'Loads data from a JSON file into the database'

    def add_arguments(self, parser):
        # Define command-line arguments here
        parser.add_argument(
            'directory',
            type=str,
            help='Path to the directory containing the JSON files'
        )

    def handle(self, *args, **options):
        # Get the models
        Object = apps.get_model('batches', 'Object')
        Batch = apps.get_model('batches', 'Batch')

        directory = options['directory']
        for filename in os.listdir(directory):
            if filename.endswith('.json'):
                with open(os.path.join(directory, filename)) as f:
                    data = json.load(f)
                    batch, _ = Batch.objects.create_or_update(batch_id=data.get('batch_id'))
                    for obj_data in data['objects']:
                        obj, _ = Object.objects.create_or_update(
                            object_id=obj_data.get('object_id'),
                            batch=batch,
                            data=obj_data.get('data'),
                        )
                        print(f'Processed {obj} from {batch}')
