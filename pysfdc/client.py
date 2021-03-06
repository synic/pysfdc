import functools
import inspect

from simple_salesforce import Salesforce

from pysfdc import exceptions, models


class Manager(object):
    def __init__(self, client, model):
        self.client = client
        self.model = model

    @property
    def _sf_interface(self):
        return getattr(self.client._salesforce, self.model._relation_name())

    def get(self, identifier=None, **kwargs):
        if not identifier and not kwargs:
            raise ValueError('You must specify a query.')

        if not identifier and len(kwargs) != 1:
            raise ValueError('You can only choose one field to query on.')

        try:
            if identifier is None:
                data = self._sf_interface.get_by_custom_id(
                    *next(iter(kwargs.items())))
            else:
                data = self._sf_interface.get(identifier)
            return self.model(self, data)
        except exceptions.SalesforceResourceNotFound:
            return None

    def __call__(self, **kwargs):
        obj = self.model(self, {})

        for key, value in kwargs.items():
            setattr(obj, key, value)

        return obj

    def create(self, **kwargs):
        obj = self(**kwargs)
        obj.save()

        return obj


class SalesForceClient(object):
    def __init__(self, **kwargs):
        self._connection_kwargs = kwargs
        self._register_default_models()

    @functools.cached_property
    def _salesforce(self):
        return Salesforce(**self._connection_kwargs)

    def register_model(self, model):
        manager = Manager(self, model)
        setattr(self, model._client_attribute_name(), manager)

    def _register_default_models(self):
        for name in dir(models):
            attr = getattr(models, name, None)
            register_model = (
                attr is not models.BaseModel
                and inspect.isclass(attr)
                and issubclass(attr, models.BaseModel)
            )

            if register_model:
                self.register_model(attr)

    @classmethod
    def create(cls, *args, **kwargs):
        return SalesForceClient(*args, **kwargs)
