from django import template
from accounts.models import Rate

register = template.Library()


@register.simple_tag()
def get_rate_dollar():
    '''Курс доллара'''
    return Rate.objects.get(currency__name_currency='Доллар').rate

@register.simple_tag()
def get_date_rate_dollar():
    '''Время послежнего обновления курса DOL по ЦБ'''
    return Rate.objects.get(currency__name_currency='Доллар').date.strftime('%d/%m %H:%M')



@register.simple_tag()
def get_rate_euro():
    '''Курс Евро'''
    return Rate.objects.get(currency__name_currency='Евро').rate

@register.simple_tag()
def get_date_rate_euro():
    '''Время послежнего обновления курса EUR по ЦБ'''
    return Rate.objects.get(currency__name_currency='Евро').date.strftime('%d/%m %H:%M')