from num2words import num2words
from django import template
from django.template.defaultfilters import stringfilter
from django.utils.safestring import mark_safe


register = template.Library()


@register.filter(needs_autoescape=True)
@stringfilter
def comma_sep_to_ul(value, autoescape=True):
    items = value.split('¬')
    lis = ['<li><p style="text-align:justify">{}</p></li>'.format(item) for item in items]
    items = '\n'.join(lis)
    items = '<ol>{}</ol>'.format(items)
    return mark_safe(items)


@register.filter(needs_autoescape=True)
@stringfilter
def comma_sep_to_li(value, autoescape=True):
    items = value.split('¬')
    lis = ['<li><p style="text-align:justify">{}</p></li>'.format(item) for item in items]
    items = '\n'.join(lis)
    return mark_safe(items)


@register.filter(needs_autoescape=True)
@stringfilter
def retain_comma(value, autoescape=True):
    items = value.split('¬')
    lis = ['{};'.format(item) for item in items]
    items = '\n'.join(lis)
    return mark_safe(items)


@register.filter(needs_autoescape=True)
def num_to_text(value, autoescape=True):
    if value:
        value = ''.join(c for c in value if c not in '$.')
        return num2words(int(value), lang='es')
    return ''
