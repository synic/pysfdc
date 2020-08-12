# :money_with_wings: SalesForce Interface Library for Python

A library aiming to add a bit of some higher level functionality to
simple-salesforce.

## Goals

1. Make interactions with SF a little easier.
2. Make the library API a little more pythonic than some of the alternatives.
3. Make the library flexible, so that it's easy to add new objects and
   relationships.

## Still To Do

The library now is mostly in a POC state. Needs to have tests added, and use
with more SF instances than the one I have.

## Requirements

* simple-salesforce (1.10.x)
* inflection (0.5.0)

## Installation

Installation using `pip` ..

    pip install git+https://github.com/synic/pysfdc

## Usage

```python

>>> from pysfdc.client import SalesForceClient
>>> sf = SalesForceClient(  # uses same arguments as simple-salesforce
...     username='myemail@example.com',
...     password='password',
...     security_token='token')
>>>
>>> contact = sf.contacts.get(email='someone@example.com')
>>> contact.id
'0033800000PzACxAAN'
>>> contact.first_name
'Some'
>>> contact.last_name
'Person'
>>>
>>> account = contact.account
>>> account.name
'Some Person, Inc.'
>>> account.phone
'(801) 867-5309'
>>>
>>> account.phone = '555-555-5555'
>>> account.save()
```
