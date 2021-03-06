import abc
import functools

import inflection


class BaseModel(abc.ABC):
    """Base model.

    .. todo:

        To make things a little more pythonic, the base model currently
        converts keys from `CamelCase` to `snake_case`. This is great for most
        one off cases, but the conversion can be expensive if you're doing a
        lot of things in bulk.

        It would be great to make it so that you can specify how to convert
        keys on the fly (or _if_ to convert, at all), or on a per-client
        basis.
    """

    def __init__(self, manager, data):
        self._sf_interface = manager._sf_interface
        self._sf_client = manager.client._salesforce
        self._client = manager.client
        self._manager = manager
        self._data = data
        self._dirty_data = {}

    @classmethod
    def _relation_name(cls):
        return cls.__name__

    @classmethod
    def _client_attribute_name(cls):
        return f'{cls._relation_name().lower()}s'

    def __getattribute__(self, key):
        exception = None
        try:
            return object.__getattribute__(self, key)
        except AttributeError as e:
            exception = e

        data_key = self.get_data_key(key)
        if data_key in self._data:
            return self._data.get(data_key)

        raise exception if exception else AttributeError(key)

    def __setattr__(self, key, value):
        if key.startswith('_'):
            super().__setattr__(key, value)
            return

        data_key = self.get_data_key(key)
        self._dirty_data[data_key] = value
        self._data[data_key] = value

    def get_data_key(self, orig_key):
        """Convert key from snake_case to CamelCase.

        Override if you need to do the conversion in some other way.
        """
        if orig_key.endswith('__c') or orig_key.endswith('__r'):
            key, suffix = orig_key.rsplit('__', 1)
            key = inflection.camelize(key)
            return f'{key}__{suffix}'

        return inflection.camelize(orig_key)

    def refresh(self):
        self._data = self._sf_interface.get(self._data['Id'])
        self._reset()

    def _reset(self):
        self._dirty_data = {}

        # reset cached properties
        for name, attr in self.__class__.__dict__.items():
            if isinstance(attr, functools.cached_property):
                try:
                    delattr(self, name)
                except AttributeError:
                    pass  # was not initialized

    def save(self):
        if not self._dirty_data:
            return

        if not self._data.get('Id'):
            res = self._sf_interface.create(self._dirty_data)
            self._data = self._dirty_data
            self.id = res['id']
            self._reset()
            return self.id

        self._sf_interface.update(self._data['Id'], self._dirty_data)
        self._reset()
        return self._data['Id']

    @functools.cached_property
    def json(self):
        return {
            inflection.underscore(key): value
            for key, value in self._data.items()
        }

    def __str__(self):
        return getattr(self, 'name', self.id)

    def __repr__(self):
        return f'<{self.__class__.__name__}: {self}>'
