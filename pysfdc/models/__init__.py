import functools

from pysfdc.models.base import BaseModel


class Lead(BaseModel):
    @functools.cached_property
    def name(self):
        return '{} {}'.format(self.first_name, self.last_name)


class User(BaseModel):
    pass


class Account(BaseModel):
    @functools.cached_property
    def owner(self):
        return self._client.users.get(self.owner_id)

    @functools.cached_property
    def parent(self):
        return self._client.accounts.get(self.parent_id)


class Contact(BaseModel):
    @functools.cached_property
    def account(self):
        return self._client.accounts.get(self.account_id)


class Opportunity(BaseModel):
    @classmethod
    def _client_attribute_name(cls):
        return 'opportunities'

    @functools.cached_property
    def account(self):
        return self._client.accounts.get(self.account_id)

    @functools.cached_property
    def owner(self):
        return self._client.users.get(self.owner_id)


class LeadStatus(BaseModel):
    @classmethod
    def _client_attribute_name(cls):
        return 'leadstatuses'
