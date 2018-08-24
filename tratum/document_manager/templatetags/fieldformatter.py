from django import template
from django.template.defaultfilters import stringfilter
from django.utils.safestring import mark_safe

register = template.Library()

@register.filter(needs_autoescape=True)
@stringfilter
def comma_sep_to_list(value, autoescape=True):
    items = value.split(',')
    lis = lambda items: [f'<li>{item}</li>' for item in items]
    items = '\n'.join(lis(items))
    html_ul = f'<ul>{items}</ul>'
    return mark_safe(html_ul)