from django import template
from django.template.defaultfilters import stringfilter
from django.utils.safestring import mark_safe

register = template.Library()

@register.filter(needs_autoescape=True)
@stringfilter
def comma_sep_to_list(value, autoescape=True):
    print(value)
    items = value.split(',')
    lis = lambda items: [f'<li>{item}</li>' for item in items]
    items = '\n'.join(lis(items))
    print(items)
    return mark_safe(items)