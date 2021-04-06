from django import template
from accounts.models import Rate

register = template.Library()


@register.simple_tag()
def get_rate_dollar():
    '''Курс доллара'''
    return Rate.objects.get(currency__name_currency='Доллар').rate

@register.simple_tag()
def get_rate_euro():
    '''Курс Евро'''
    return Rate.objects.get(currency__name_currency='Евро').rate