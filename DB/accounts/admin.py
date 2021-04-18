from django.contrib import admin
from .models import Telephone, TypeNumber, Country, Area, City, UserLocation, \
    Score,Balance,Currency,BankName,Swift, Credit, InterestRate, Payments,Rate, \
    Card, PaymentSystem, TypeCard, CreditTarget


@admin.register(TypeNumber)
class TypeNumberAdmin(admin.ModelAdmin):
    '''Тип номера'''
    list_display = ("type_number",)

@admin.register(Telephone)
class TelephoneAdmin(admin.ModelAdmin):
    '''Телефон'''
    list_display = ("telephone_number","user_id", "get_type_number")

@admin.register(City)
class CityAdmin(admin.ModelAdmin):
    '''Город'''
    list_select_related = True

@admin.register(Credit)
class CreditAdmin(admin.ModelAdmin):
    '''Телефон'''
    list_display = ("user_id","sum_credit")



admin.site.register(Country)
admin.site.register(Area)
admin.site.register(UserLocation)
admin.site.register(Score)
admin.site.register(Balance)
admin.site.register(Currency)
admin.site.register(BankName)
admin.site.register(Swift)
admin.site.register(InterestRate)
admin.site.register(Payments)
admin.site.register(Rate)
admin.site.register(Card)
admin.site.register(PaymentSystem)
admin.site.register(TypeCard)
admin.site.register(CreditTarget)




# Register your models here.
