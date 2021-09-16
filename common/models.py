""" This contains default implementation of models used accross this project
"""
from django.db import models
from django.utils import timezone


class BaseModel(models.Model):
    """Base Model with default fields"""

    created_at = models.DateTimeField(db_index=True, auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True
