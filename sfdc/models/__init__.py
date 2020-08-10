import functools

from .base import BaseModel


class Lead(BaseModel):
    @functools.cached_proprty
    def name(self):
        return '{} {}'.format(self.first_name, self.last_name)


class User(BaseModel):
    pass


class Account(BaseModel):
    @functools.cached_proprty
    def owner(self):
        return self._client.users.get(self.owner_id)

    @functools.cached_proprty
    def parent(self):
        return self._client.accounts.get(self.parent_id)

    def _get_data_key(self, key):
        if key == 'account_type__c':
            return 'Account_Type__c'
        return super()._get_data_key(key)


class Contact(BaseModel):
    @functools.cached_proprty
    def account(self):
        return self._client.accounts.get(self.account_id)


class Opportunity(BaseModel):
    @classmethod
    def _client_attribute_name(cls):
        return 'opportunities'

    @functools.cached_proprty
    def account(self):
        return self._client.accounts.get(self.account_id)

    @functools.cached_proprty
    def owner(self):
        return self._client.users.get(self.owner_id)


class LeadStatus(BaseModel):
    @classmethod
    def _client_attribute_name(cls):
        return "leadstatuses"
