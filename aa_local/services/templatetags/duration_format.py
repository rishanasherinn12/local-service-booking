from django import template

register = template.Library()

@register.filter
def duration_format(minutes):
    minutes = int(minutes)

    hours = minutes // 60
    remaining = minutes % 60

    if hours > 0 and remaining > 0:
        return f"{hours} hr {remaining} min"
    elif hours > 0:
        return f"{hours} hr"
    else:
        return f"{remaining} min"