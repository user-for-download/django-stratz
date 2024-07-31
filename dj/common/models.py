from datetime import datetime
from uuid import uuid4

from django.db import models
from django.utils import timezone

from dj.common.utils import get_delta_time


class BaseManager(models.Manager):
    def active(self):
        return self.get_queryset().filter(deleted_at__isnull=True)


class BaseModel(models.Model):
    uuid = models.UUIDField(primary_key=True, default=uuid4, editable=False)
    created_at = models.DateTimeField(db_index=True, default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)
    deleted_at = models.DateTimeField(blank=True, null=True)

    objects = BaseManager()

    class Meta:
        abstract = True

    def save(self, *args, **kwargs):
        if not self.pk:  # If it's a new object
            self.created_at = datetime.now()
        self.updated_at = datetime.now()
        super(BaseModel, self).save(*args, **kwargs)

    def delete(self, using=None, keep_parents=False):
        self.deleted_at = datetime.now()
        self.save()

    def restore(self):
        self.deleted_at = None
        self.save()

    def get_last_update(self) -> str:
        return get_delta_time(self.updated_at)

    @classmethod
    def active_objects(cls):
        return cls.objects.filter(deleted_at__isnull=True)
