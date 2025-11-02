import re
from decimal import Decimal, InvalidOperation

from django.db import models
from django.db.models.functions import Concat


def increase_slug_by_one(slug: str) -> str:
    if not slug:
        return slug

    slug = slug.lower()
    pattern = re.compile(r"([^0-9]*)(\d+)$")
    match_obj = pattern.match(slug)

    if match_obj:
        number = int(match_obj.groups()[-1]) + 1
        string = match_obj.groups()[0]
        increased_slug = f"{string}{number}"
    else:
        increased_slug = f"{slug}1"

    return increased_slug


def get_differences(from_: dict, to: dict) -> dict:
    """Return the differences between two dictionaries."""
    differences: set = set(from_.items()) ^ set(to.items())

    before: dict = {}
    after: dict = {}

    for key, value in differences:
        diff = key, value
        if diff in from_.items():
            before[key] = value
        else:
            after[key] = value

    if differences:
        return {"before": before, "after": after}

    return {}


def get_keywords_query(
    value: str,
    *,
    field_name: str = "search",
) -> models.Q:
    """Return a search query."""
    query: models.Q = models.Q()
    keywords = value.split(" ")

    for word in keywords:
        kwargs = {f"{field_name}__icontains": word}
        query &= models.Q(**kwargs)

    return query


def annotate_search(*fields: str) -> Concat:
    fields = fields * 2

    args: list[models.F | models.Value] = []

    for field in fields:
        args.append(models.F(field))
        args.append(models.Value(" "))

    return Concat(*args[:-1], output_field=models.CharField())


def parse_decimal(value: str) -> Decimal:
    number = value.replace(",", "")

    try:
        number = Decimal(number)
    except InvalidOperation:
        number = Decimal(0)

    return number
