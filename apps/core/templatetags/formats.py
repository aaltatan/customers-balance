from decimal import Decimal
from typing import Literal

from django import template
from django.utils.html import format_html

register = template.Library()


def _format_string(
    value: str,
    *,
    chars_width: int = 15,
    in_table: bool = False,
    color: Literal["red", "green", "none"] = "none",
) -> str:
    right_result = value.rjust(chars_width)
    left_result = value.ljust(chars_width)

    text_color = "" if color == "none" else f"style='color: {color}'"

    if in_table:
        return format_html(
            """
            <pre {text_color} class='rtl:hidden @max-lg:hidden font-medium'>{right_result}</pre>
            <pre {text_color} class='ltr:hidden @max-lg:hidden font-medium'>{left_result}</pre>
            <pre {text_color} class='@lg:hidden font-medium'>{value}</pre>
            """,
            text_color=text_color,
            right_result=right_result,
            left_result=left_result,
            value=value,
        )

    return format_html("<pre {text_color} class='font-medium'>{value}</pre>", text_color=text_color, value=value)


@register.filter
def percentage(
    value: float | Decimal,
    *,
    in_table: bool = False,
    decimal_places: int = 2,
) -> str:
    result = f"{value * 100:.{decimal_places}f} %"
    return _format_string(result, in_table=in_table, chars_width=10)


@register.filter
def money(
    value: float | Decimal | str,
    *,
    in_table: bool = False,
    decimal_places: int = 2,
    chars_width: int = 15,
) -> str:
    if not value:
        return _format_string("0", in_table=in_table, chars_width=chars_width)

    if not isinstance(value, str):
        if value < 0:
            value = abs(value)
            result = f"({value:,.{decimal_places}f})"
        else:
            result = f"{value:,.{decimal_places}f}"

    return _format_string(
        result,
        in_table=in_table,
        chars_width=chars_width,
    )
