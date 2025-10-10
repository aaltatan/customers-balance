from django.db.models import DecimalField

from .validators import (
    decimal_min_value_validator,
    rate_max_value_validator,
    rate_min_value_validator,
)


class MoneyField(DecimalField):
    def __init__(self, *args, **kwargs):
        kwargs.setdefault("max_digits", 24)
        kwargs.setdefault("decimal_places", 4)
        kwargs.setdefault("validators", [decimal_min_value_validator])
        super().__init__(*args, **kwargs)


class PercentageField(DecimalField):
    def __init__(self, *args, **kwargs):
        kwargs.setdefault("max_digits", 10)
        kwargs.setdefault("decimal_places", 6)
        kwargs.setdefault(
            "validators",
            [
                rate_min_value_validator,
                rate_max_value_validator,
            ],
        )
        super().__init__(*args, **kwargs)
