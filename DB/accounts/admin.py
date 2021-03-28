from django.contrib import admin
from .models import Telephone, TypeNumber, Country, ResidenceAddres, Area, City, Location


@admin.register(TypeNumber)
class TypeNumberAdmin(admin.ModelAdmin):
    '''Тип номера'''
    list_display = ("type_number",)

@admin.register(Telephone)
class TelephoneAdmin(admin.ModelAdmin):
    '''Телефон'''
    list_display = ("telephone_number","user_id", "get_type_number")


admin.site.register(Country)
admin.site.register(ResidenceAddres)
admin.site.register(Area)
admin.site.register(City)
admin.site.register(Location)



# Register your models here.
