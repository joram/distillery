from django import template

register = template.Library()


@register.simple_tag
def timedelta(delta):
    print delta
    hours, remainder = divmod(delta, 3600)
    minutes, seconds = divmod(remainder, 60)
    return '%d:%d:%d' % (hours, minutes, seconds)
