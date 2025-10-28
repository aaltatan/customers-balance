from typing import Generic, TypeVar, ClassVar

from django.contrib.contenttypes.models import ContentType
from django.db import models, transaction
from rest_framework import serializers

from apps.core.models import Activity, User
from apps.core.protocols import Saveable
from apps.core.utils import get_differences


ModelType = TypeVar("ModelType", bound=models.Model)


class Service(Generic[ModelType]):
    model_class = ClassVar[type[models.Model]]

    @classmethod
    @transaction.atomic
    def add(cls, user: User, saver: Saveable[ModelType]) -> ModelType:
        instance = saver.save()
        Activity(
            user=user,
            kind=Activity.KindChoices.ADD,
            object_id=instance.pk,
            content_type=ContentType.objects.get_for_model(cls.model_class),
        ).save()

        return instance

    @classmethod
    @transaction.atomic
    def change(
        cls,
        user: User,
        serializer_class: type[serializers.ModelSerializer],
        saver: Saveable[ModelType],
        instance: ModelType,
    ) -> ModelType:
        Model = instance.__class__
        old_instance = Model.objects.get(pk=instance.pk)

        old_instance_data = serializer_class(old_instance).data

        instance = saver.save()

        instance_data = serializer_class(instance).data
        data = get_differences(old_instance_data, instance_data)

        Activity(
            user=user,
            kind=Activity.KindChoices.CHANGE,
            object_id=instance.pk,
            data=data,
            content_type=ContentType.objects.get_for_model(cls.model_class),
        ).save()

        return instance
    
    @classmethod
    @transaction.atomic
    def delete(
        cls,
        user: User,
        instance: ModelType,
        serializer_class: type[serializers.ModelSerializer],
    ) -> None:
        data = serializer_class(instance).data
        instance_pk = instance.pk

        instance.delete()

        Activity(
            user=user,
            kind=Activity.KindChoices.DELETE,
            object_id=instance_pk,
            data=data,
            content_type=ContentType.objects.get_for_model(cls.model_class),
        ).save()