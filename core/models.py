from django.db import models
import uuid


class VersionedModel(models.Model):
    """ Abstract base class for versioned models. """
    version = models.IntegerField(default=1)
    is_deleted = models.BooleanField(default=False)

    class Meta:
        abstract = True


class ExtendableModel(models.Model):
    """ Abstract base class for models with extensibility. """
    extended_data = models.JSONField(null=True, blank=True)

    class Meta:
        abstract = True


class UUIDModel(models.Model):
    """ Abstract base class for models that use UUIDs. """
    uuid = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)

    class Meta:
        abstract = True


class ObjectMutation(models.Model):
    """ Abstract base class for handling mutations on objects. """
    mutation_date = models.DateTimeField(auto_now_add=True)
    mutation_user_id = models.IntegerField()

    class Meta:
        abstract = True


class MutationLog(models.Model):
    """ Model to log changes (mutations) in other models. """
    mutation_type = models.CharField(max_length=255)
    mutation_date = models.DateTimeField(auto_now_add=True)
    description = models.TextField(null=True, blank=True)
    user_id = models.IntegerField()

    class Meta:
        db_table = 'core_mutationlog'


class ModuleConfiguration(models.Model):
    DoesNotExist = None
    objects = None
    module = models.CharField(max_length=255, unique=True)
    is_enabled = models.BooleanField(default=False)
    configuration = models.JSONField(default=dict)

    @classmethod
    def get_or_default(cls, module_name, default_cfg):
        try:
            config = cls.objects.get(module=module_name)
            return config.configuration
        except cls.DoesNotExist:

            return default_cfg
