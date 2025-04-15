from django.db.models.manager import BaseManager
from django.db import models
from uuid import uuid4


class MenuManager(models.Manager):
    def create(self, **kwargs):
        name = kwargs.get('name')
        if name:
            key = name.lower().replace(' ', '_') + str(uuid4())[:2]
            kwargs['key'] = key
        return super().create(**kwargs)