from django.core.validators import (
    MaxValueValidator,
    MinLengthValidator,
    MinValueValidator,
    RegexValidator,
)
from django.utils.translation import gettext_lazy as _

four_char_validator = MinLengthValidator(4, _("field must be 4 characters at least"))
syrian_mobile_validator = RegexValidator(
    r"^09\d{8}$", _("mobile number's pattern must be like 0933222111")
)

rate_min_value_validator = MinValueValidator(
    0, message=_("Value must be greater than or equal to 0")
)
rate_max_value_validator = MaxValueValidator(
    1, message=_("Value must be less than or equal to 1")
)

decimal_min_value_validator = MinValueValidator(
    0, message=_("Value must be greater than or equal to 0")
)
