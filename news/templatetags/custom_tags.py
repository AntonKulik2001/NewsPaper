from datetime import datetime
from django import template
from news.models import Post


register = template.Library()

@register.simple_tag()
def date_create(format_string='%d %m %Y'):
    return datetime.utcnow().strftime(format_string)

@register.simple_tag(takes_context=True)
def url_replace(context, **kwargs):
    d = context['request'].GET.copy()
    for k, v in kwargs.items():
        d[k] = v
    return d.urlencode()