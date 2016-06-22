from randomcomposer.modules.storage.composer import Composer
from uuid import uuid4
from randomcomposer.modules.exceptions import RequiredAttributeMissing, ItemAlreadyExists, ItemDoesNotExist


class ComposerApi:
    required_params = ['name']
    optional_params = ['wikipedia', 'viaf']

    def create(self, data):
        cleaned_data = self.check_required(data)

    def read(self, uuid):
        existing_composer = Composer.objects(uuid=uuid).first()
        if existing_composer is None:
            raise ItemDoesNotExist('No item with uuid {0}!'.format(uuid))
        return existing_composer

    def update(self, uuid, data):
        cleaned_data = self.check_required(data)
        existing_composer = self.read(uuid)

    def delete(self, uuid):
        existing_composer = self.read(uuid)

    def check_required(self, data):
        cleaned_data = {}
        for param in self.required_params + self.optional_params:
            if param in data:
                cleaned_data[param] = data[param]
            else:
                if param in self.required_params:
                    raise RequiredAttributeMissing('Missing attribute {0} missing!'.format(param))
        return cleaned_data
