from django import template
from django.template.defaultfilters import stringfilter
from django.utils.safestring import mark_safe

register = template.Library()

@register.filter(needs_autoescape=True)
@stringfilter
def comma_sep_to_ul(value, autoescape=True):
    items = value.split(',')
    lis = lambda items: [f'<li><p style="text-align:justify">{item}</p></li>' for item in items]
    items = '\n'.join(lis(items))
    items = f'<ul>{items}</ul>'
    return mark_safe(items)


@register.filter(needs_autoescape=True)
@stringfilter
def comma_sep_to_li(value, autoescape=True):
    items = value.split(',')
    lis = lambda items: [f'<li>{item}</li>' for item in items]
    items = '\n'.join(lis(items))
    return mark_safe(items)