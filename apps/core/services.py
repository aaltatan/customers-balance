from typing import TypeVar

from django.contrib.contenttypes.models import ContentType
from django.db import models, transaction
from rest_framework.serializers import ModelSerializer

from apps.core.models import Activity, User
from apps.core.protocols import Saveable
from apps.core.utils import get_differences

ModelType = TypeVar("ModelType", bound=models.Model)


@transaction.atomic
def add_instance(user: User, saver: Saveable[ModelType]) -> ModelType:
    instance = saver.save()
    Activity(
        user=user,
        kind=Activity.KindChoices.ADD,
        object_id=instance.pk,
        content_type=ContentType.objects.get_for_model(saver.Meta.model),
    ).save()

    return instance


@transaction.atomic
def change_instance(
    user: User,
    serializer_class: type[ModelSerializer],
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
        content_type=ContentType.objects.get_for_model(saver.Meta.model),
    ).save()

    return instance


@transaction.atomic
def delete_instance(
    user: User, instance: models.Model, serializer_class: type[ModelSerializer]
) -> None:
    data = serializer_class(instance).data
    instance_pk = instance.pk

    instance.delete()

    Activity(
        user=user,
        kind=Activity.KindChoices.DELETE,
        object_id=instance_pk,
        data=data,
        content_type=ContentType.objects.get_for_model(instance.__class__),
    ).save()
