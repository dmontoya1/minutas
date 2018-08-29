from django import template
from django.template.defaultfilters import stringfilter
from django.utils.safestring import mark_safe


register = template.Library()

@register.filter(needs_autoescape=True)
@stringfilter
def comma_sep_to_ul(value, autoescape=True): 
    items = value.split('¬')
    lis = lambda items: [f'<li><p style="text-align:justify">{item}</p></li>' for item in items]
    items = '\n'.join(lis(items))
    items = f'<ol>{items}</ol>'
    return mark_safe(items)


@register.filter(needs_autoescape=True)
@stringfilter
def comma_sep_to_li(value, autoescape=True):
    print(value)
    items = value.split('¬')
    print(items)
    lis = lambda items: [f'<li><p style="text-align:justify">{item}</p></li>' for item in items]
    items = '\n'.join(lis(items))
    return mark_safe(items)